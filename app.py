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

temp=0;
humid=0;

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
                value=temp,
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
                interval=500,
                n_intervals=0,
            )
            # html.Button(children='Switch', n_clicks=0, id='button-on-and-off'),
        ],className="card"),
        html.Div(children=[
            daq.Gauge(
                label='Humidity',
                id='humidity',
                min=0,
                max=100,
                value=humid,
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
            # html.Button(children='Switch', n_clicks=0, id='button-on-and-off'),
        ],className="card"),
        html.Div(children=[
            html.Img(id='fan', src=LED_OFF),
            html.Button(children='Switch', n_clicks=0, id='fan-on-and-off'),
            dcc.Interval(
                id='fan_frame',
                interval=1000,
                n_intervals=0,
                max_intervals=60000
            ),
        ],className="card"),
    ],className='main'),
])
@app.callback(
    #adding an array means the input or output must contain an array
    [Output('bulb', 'src'),Output('light-on-and-off', 'className')],
    Input('light-on-and-off', 'n_clicks')
)
def update_LED (n_clicks):
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
    if(n % 2 == 0):
        # return DHT11.read()
        return [(n / 3), n] # tresting
    return
    
@app.callback(
        [Output('fan', 'src'),Output('fan-on-and-off', 'className')],
        Input('fan-on-and-off', 'n_clicks')
)
def update_FAN(n_clicks):
    click = n_clicks % 2
    if click:
        # DC Turn on for testing
        return [LED_ON,'toggleOn']
    else:
        # DC Turn off for testing
        return [LED_OFF,'toggleOff']

# live checking to turn on and off dc motor here
#TODO: check for 24 Degrees Cel then send email then receive then turn on if yes, keep it off otherwise, it has a timer of 1 minute for the reply
def turnFan():
    return

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    app.run(debug=True)
    