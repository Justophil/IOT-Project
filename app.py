from dash import Dash, html, callback, Output, Input, dcc
import dash_daq as daq
import LED
import DHT11
import Emails as MAIL
import DCMotor as DC
import Mqtt as MQTT
import SQLite as SQL

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
SQL = SQL.SQLite()
SQL.connect()

not_sent=1
not_sent2=1
has_replied=0
fan_status=0
tempera=0
light_status=0
light=0
sent_notification=0
timer=0
maxTimer=0
temp_thr=24
humid_thr=60
lightintensity_thr=400
user_id=""
app.layout = html.Div([
    html.Div(children=[
        html.H2('Dashboard'),
    ], className="header"),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src='',className="user-icon")
                ], className='main-header-column'),
                html.Div(children=[
                    html.Label(children="ID:",className="user-label"),
                    dcc.Interval(
                        id="user-id-frame",
                        interval=1000,
                        n_intervals=0
                    ),
                    html.Label(children="Name:",className="user-label"),
                    html.Label(children="Temperature Threshold:",className="user-label"),
                    html.Label(children="Humidity Threshold:",className="user-label"),
                    html.Label(children="Light Intensity Threshold:",className="user-label"),
                ], className='main-header-column'),
                html.Div(children=[
                    html.Label(id="user-id",className="user-label"),
                    dcc.Input(id="user-name",type="text",placeholder="Name",className="user-input"),
                    dcc.Input(id="user-temp",type="text",placeholder="Temperature",className="user-input"),
                    dcc.Input(id="user-humid",type="text",placeholder="Humidity",className="user-input"),
                    dcc.Input(id="user-light-intensity",type="text",placeholder="Light Intensity",className="user-input"),
                ], className='main-header-column'),
                html.Div(children=[
                    dcc.Interval(
                        id="notif-frame",
                        interval=1000,
                        n_intervals=0
                    ),
                    html.Div(children=[
                        html.H3("Note: A notification has been sent to you by email"),
                    ],id="notif-card",className="notif",hidden=True),
                ], className='main-header-column'),
            ],className="user-card")
        ],className="main-header"),
        html.Div(children=[
            # html.Div(children=[
            #     html.Img(id='bulb', src=LED_OFF, className="icon"),
            #     html.Button(children='Switch', n_clicks=0, id='light-on-and-off'),
            # ],className="card"),
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
                html.H3(id="light-intensity-label", children=123),
                daq.Slider(min=0,max=1000,value=0,id="intensity-slider",size=200,disabled=True),
                dcc.Interval(
                    id='light_intensity_frame',
                    interval=1000,
                    n_intervals=0,
                )
            ],className="card"),
            html.Div(children=[
                html.Img(id='bluetooth', src=LED_OFF, className="icon"),
                html.H3(children=0,id="bluetooth-counter"),
            ],className="card",)
        ],className="main-content"),
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
    global temp_thr
    if (temp <= temp_thr and not not_sent):
        not_sent=1
    if temp > temp_thr and not_sent:
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
        
    if fan_status and temp > temp_thr:
        return [FAN_ON]
    elif temp <= temp_thr or not fan_status:
        if temp <= temp_thr:
            has_replied=0
        fan_status = 0
        DC.turn_off()
        return [FAN_OFF]
@app.callback(
    [Output('light-intensity-label', 'children'), Output('intensity-slider', 'value')],
    # Output('light-intensity-label', 'children'),
    Input('light_intensity_frame', 'n_intervals')
)
def updateIntensity(n_intervals):
    intensity = int(MQTT.light)
    return [intensity, intensity]
    # return intensity
    
@app.callback(
    Output('light-intensity', 'src'),
    Input('light-intensity-label', 'children')
)
def updateLight(intensity):
    global sent_notification
    global light_status
    global lightintensity_thr
    if(intensity < lightintensity_thr):
        sent_notification = 1
        return LED_ON
    else:
        sent_notification=0
        light_status=0
        return LED_OFF
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
    global sent_notification
    global not_sent2
    global light_status
    if(sent_notification and (timer == 0) and not light_status):
        timer+=n_intervals
        maxTimer+=(n_intervals + 10)
        light_status = 1
        return False
    if(timer <= maxTimer and timer != maxTimer):
        if(not_sent2):
            not_sent2=0  
            MAIL.setMessages(0)
            MAIL.send("notification")      
        timer+=1
        return False
    else:
        not_sent2=1
        timer=0
        maxTimer=0
        return True

@app.callback(
    Output('user-id', 'children'),
    Input('user-id-frame', 'n_intervals')
)
def updateUserId(n):
    global user_id
    if(MQTT.rfid is None):
        return ""
    SQL.user_id = MQTT.rfid
    if(SQL.getUser() is None):
        SQL.createUser()
    if(SQL.user_id is not user_id):
        user_id = SQL.user_id
    return SQL.user_id
    
@app.callback(
    Output('user-name', 'value'),
    Input('user-name', 'value')
)
def updateName(name):
    SQL.name = name
    SQL.updateUser()
    return name

@app.callback(
    Output('user-temp', 'value'),
    Input('user-temp', 'value')
)
def updateTemp(temp):
    if(not temp.isnumeric()):
        return temp
    SQL.temp_thr = temp
    SQL.updateUser()
    return temp

@app.callback(
    Output('user-humid', 'value'),
    Input('user-humid', 'value')
)
def updateHumi(humi):
    if(not humi.isnumeric()):
        return humi
    SQL.humid_thr = humi
    SQL.updateUser()
    return humi

@app.callback(
    Output('user-light-intensity', 'value'),
    Input('user-light-intensity', 'value')
)
def updateLigh(ligh):
    if(not ligh.isnumeric()):
        return ligh
    SQL.lightintensity_thr = ligh
    SQL.updateUser()
    return ligh

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    MQTT.run()
    app.run(debug=True)