from dash import Dash, html, callback, Output, Input, dcc
import dash_daq as daq
import LED
import DHT11
import Emails as MAIL
import DCMotor as DC

app = Dash(__name__)

LED_ON = '/assets/img/led_on.png'
LED_OFF = '/assets/img/led_off.png'
FAN_ON = '/assets/img/fan_on.png'
FAN_OFF = '/assets/img/fan_off.png'

LEDPin=23
DHT11Pin=18 #! BOARD PIN
ENABLEDC=17
INPUT1DC=22
INPUT2DC=27

LED = LED.LED(LEDPin)
DC = DC.DCMotor(ENABLEDC, INPUT1DC, INPUT2DC)
DHT11 = DHT11.DHT11(DHT11Pin)
MAIL = MAIL.Email()

not_sent=1
has_replied=0
fan_status=0

app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard'),
    ], className="header"),
    html.Div(children=[
        html.Div(children=[
            html.Img(id='bulb', src=LED_OFF, className="icon"),
            html.Button(children='Switch', n_clicks=0, id='light-on-and-off'),
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
    return DHT11.read()
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
    if (temp < 24 and not not_sent):
        not_sent=1
    if temp >= 24 and not_sent:
        not_sent=0
        # Send email
        MAIL.send()
        print('email sent')
        # Wait for the user's response
        response_received = False
        response_timer = 0
        while not response_received and response_timer < 60 and not has_replied:
            # Receive email response
            response_received = MAIL.receive()
            response_timer += 1
            if MAIL.original_email <= MAIL.reply_email:
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
        
    if fan_status and temp >= 24:
        return [FAN_ON]
    elif temp < 24 or not fan_status:
        if temp < 24:
            has_replied=0
        fan_status = 0
        DC.turn_off()
        return [FAN_OFF]

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    app.run(debug=True)
    