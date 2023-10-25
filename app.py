from dash import Dash, html, callback, Output, Input, dcc
import dash_daq as daq
import LED
import DHT11
import Emails as MAIL
import DCMotor as DC

app = Dash(__name__)

LED_ON = '/assets/img/on.png'
LED_OFF = '/assets/img/off.png'

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
fan_status=0

app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard'),
    ], className="header"),
    html.Div(children=[
        html.Div(children=[
            html.Img(id='bulb', src=LED_OFF),
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
            html.Img(id='fan', src=LED_OFF),
            # html.Button(children='Switch', n_clicks=0, id='fan-on-and-off'),
            # dcc.Interval(
            #     id='fan_frame',
            #     interval=1000,
            #     n_intervals=60,
            # ),
        ],className="card"),
    ],className='main'),
])
@app.callback(
    #adding an array means the input or output must contain an array
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
    # return DHT11.read()
    return [n, n]

# live checking to turn on and off dc motor here
# @app.callback(
#         [Output('fan', 'src'),Output('fan-on-and-off', 'className')],
#         Input('fan-on-and-off', 'n_clicks')
# )
# def switchFan(n_clicks):
#     click = n_clicks % 2
#     if click:
#         # DC Turn on for testing
#         DC.turn_on()
#         return [LED_ON,'toggleOn']
#     else:
#         # DC Turn off for testing
#         DC.turn_off()
#         return [LED_OFF,'toggleOff']

# live checking to turn on and off dc motor here
#TODO: check for 24 Degrees Cel then send email then receive then turn on if yes, keep it off otherwise, it has a timer of 1 minute for the reply
@app.callback(
    # [Output('fan_frame', 'n_intervals'),Output('fan', 'src'),Output('fan-on-and-off', 'className')],
    # [Output('fan', 'src'),Output('fan-on-and-off', 'className')],
    [Output('fan', 'src')],
    # [Input('temperature', 'value'), Input('fan_frame', 'n_intervals')]
    [Input('temperature', 'value')]
)
def updateFan(temp):
    global not_sent
    global fan_status
    print(not_sent)
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
        while not response_received and response_timer < 60:
            # Receive email response
            response_received = MAIL.receive()
            response_timer += 1
        print(response_received)
        if response_received:
            # User replied "yes", turn on the motor
            print('on')
            DC.turn_on()
            fan_status = 1
            # return [0, LED_ON, 'toggleOn']
            # return [LED_ON, 'toggleOn']
            return [LED_ON]
        else:
            # User did not reply or replied "no", turn off the motor
            print('off')
            DC.turn_off()
            fan_status = 0
            # return [0,LED_OFF, 'toggleOff']
            # return [LED_OFF, 'toggleOff']
            return [LED_OFF]
    if fan_status and temp >= 24:
        return [LED_ON]
    elif temp < 24 or not fan_status:
        fan_status = 0
        DC.turn_off()
        return [LED_OFF]

    # DC.turn_off()
    # # return [n_intervals,LED_OFF, 'toggleOff']
    # # return [LED_OFF, 'toggleOff']
    # return [LED_OFF]

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    app.run(debug=True)
    