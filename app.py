from dash import Dash, html, callback, Output, Input, dcc
import dash_daq as daq
import LED
import DHT11
import Emails as MAIL
import DCMotor as DC
import Mqtt as MQTT

app = Dash(__name__)

LED_ON = '/assets/img/led_on.png'
LED_OFF = '/assets/img/led_off.png'
FAN_ON = '/assets/img/fan_on.png'
FAN_OFF = '/assets/img/fan_off.png'

LEDPin=23
DHT11Pin=24
ENABLEDC=17
INPUT1DC=22
INPUT2DC=27

LED = LED.LED(LEDPin)
DC = DC.DCMotor(ENABLEDC, INPUT1DC, INPUT2DC)
DHT11 = DHT11.DHT11(DHT11Pin)
MAIL = MAIL.Email()
MQTT = MQTT.Mqtt()

not_sent=1
has_replied=0
fan_status=0
tempera=0
light_status=0
light=0
sent_notification=0
timer=0
maxTimer=0
app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard'),
    ], className="header"),
    html.Div(children=[
        html.H3(children="Note: A notification has been sent to you by email"),
        dcc.Interval(
                id="notif-frame",
                interval=1000,
                n_intervals=0
            )
    ],id="notif-card",className="notif",hidden=True),
    html.Div(children=[
        html.Div(children=[
            html.Img(id='bulb', src=LED_OFF, className="icon"),
            html.Button(children='Switch', n_clicks=0, id='light-on-and-off', disabled=True),
        ],className="card"),
        html.Div(children=[
            daq.Gauge(
                label='Temperature',
                id='temperature',
                min=0,
                max=40,
                value=0,
                className="icon",
                showCurrentValue=True,
                units="C",
                color={
                    'gradient':True,
                    'ranges':{
                        'green':[0, 10],
                        'yellow':[10, 20],
                        'orange':[20, 30],
                        'red':[30, 40],
                    }
                }
            ),
            dcc.Interval(
                id='dht_frame',
                interval=1000,
                n_intervals=0,
            )
        ],className="card"),
        html.Div(children=[
            daq.Gauge(
                label='Humidity',
                id='humidity',
                min=0,
                max=100,
                value=0,
                className="icon",
                showCurrentValue=True,
                units="%",
                color={
                    'gradient':True,
                    'ranges':{
                        'green':[0, 25],
                        'yellow':[25, 50],
                        'orange':[50, 75],
                        'red':[75, 100],
                    }
                }
            ),
        ],className="card"),
        html.Div(children=[
            html.Img(id='fan', src=FAN_OFF, className="icon"),
        ],className="card"),
        html.Div(children=[
            html.Img(id='light-intensity', src=LED_OFF, className="icon"),
            html.H3(id="light-intensity-label", children=0),
            dcc.Slider(0,1000,100,value=0,id="intensity-slider"),
            dcc.Interval(
                id='light_intensity_frame',
                interval=1000,
                n_intervals=0,
            )
        ],className="card")
    ],className='main'),
])

#Live checking for button input to turn on the LED or off
@app.callback(
    [Output('bulb', 'src'),Output('light-on-and-off', 'className')],
    Input('light-on-and-off', 'n_clicks')
)
def updateLED (n_clicks):
    click = n_clicks % 2
    if click:
        LED.turn_on()
        return [LED_ON,'toggleOn']
    else:
        LED.turn_off()
        return [LED_OFF,'toggleOff']
# live checking for data change
@app.callback(
    [Output('temperature', 'value'), Output('humidity', 'value')],
    Input('dht_frame','n_intervals')
)
def updateDHT(n):
    global tempera
    temp = DHT11.read()
    tempera = temp[0]
    return temp
    # tempera = 24.5
    # return [n, n]

# live checking to turn on and off dc motor here
@app.callback(
    [Output('fan', 'src')],
    [Input('temperature', 'value')]
)
def updateFan(temp):
    global not_sent
    global fan_status
    global has_replied
    global tempera
    if (temp <= 24 and not not_sent):
        not_sent=1
    if temp > 24 and not_sent:
        not_sent=0
        MAIL.setMessages(tempera)
        # Send email
        MAIL.send("message")
        # Wait for the user's response
        response_received = False
        response_timer = 0
        while not response_received and response_timer < 60 and not has_replied:
            # Receive email response
            response_received = MAIL.receive()
            response_timer += 1
            if MAIL.original_email < MAIL.reply_email:
                has_replied=1
        if response_received:
            # User replied "yes", turn on the motor
            DC.turn_on()
            fan_status = 1
            return [FAN_ON]
        else:
            # User did not reply or replied "yes", turn off the motor
            DC.turn_off()
            fan_status = 0
            return [FAN_OFF]
        
    if fan_status and temp > 24:
        return [FAN_ON]
    elif temp <= 24 or not fan_status:
        if temp <= 24:
            has_replied=0
        fan_status = 0
        DC.turn_off()
        return [FAN_OFF]
@app.callback(
    [Output('light-intensity-label', 'children'), Output('intensity-slider', 'value')],
    Input('light_intensity_frame', 'n_intervals')
)
def updateIntensity(n_intervals):
    MQTT.subscribe()
    intensity = MQTT.data['light']
    print(intensity)
    return [intensity, intensity]
    
@app.callback(
    Output('light-intensity', 'src'),
    Input('light-intensity-label', 'children')
)
def updateLight(intensity):
    global sent_notification
    if(intensity < 400):
        MAIL.send("notification")
        sent_notification = 1
        light_status = 1
        LED.turn_on()
        return [LED_ON]
    else:
        LED.turn_off()
        return [LED_OFF]
    # if(light_status):
    #     LED.turn_on()
    #     return [LED_ON]
    # else:
    #     LED.turn_off()
    #     return [LED_OFF]
@app.callback(
    Output('notif-card', 'hidden'),
    Input('notif-frame', 'n_intervals')
)
def updateNotif(n_intervals):
    global timer
    global maxTimer
    if(sent_notification and timer == 0):
        timer+=n_intervals
        maxTimer+=(n_intervals + 10)
        return False
    if(timer <= maxTimer and timer != maxTimer):
        timer+=1
        return False
    else:
        sent_notification=0
        timer=0
        maxTimer=0
        return True

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    app.run(debug=True)