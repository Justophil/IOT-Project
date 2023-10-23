from dash import Dash, html, callback, Output, Input
import dash_daq as daq
# import RPi.GPIO as GPIO
# import time as sleep
import smtplib
import ssl

app = Dash(__name__)

LED_ON = '/assets/img/on.png'
LED_OFF = '/assets/img/off.png'

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering
# LED=17
# GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

# Setup port number and servr name

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

email_from = "phildschool@gmail.com"
email_to = "phildschool@gmail.com"

pswd = 'vjty nkvt olic dvsd'

message = """From: From IOT-Dashboard <iotdashboard@iotDash.com>
To: Phil <phildschool@gmail.com>
Subject: Notice! the room is getting hot


Would you like to turn on the fan?
if yes, reply to this email with a yes
"""    

simple_email_context = ssl.create_default_context()

app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard'),
    ], className="header"),
    html.Div(children=[
        html.Div(children=[
            html.Img(id='bulb', src=LED_OFF),
            html.Button(children='Switch', n_clicks=0, id='light-on-and-off'),
            html.Button(children='Send Email', n_clicks=0, id='button-send-email'),
        ],className="card"),
        html.Div(children=[
            # html.Img(id='bulb', src=LED_OFF),
            # html.Button(children='Switch', n_clicks=0, id='button-on-and-off'),
        ],className="card"),
        html.Div(children=[
            # html.Img(id='bulb', src=LED_OFF),
            # html.Button(children='Switch', n_clicks=0, id='button-on-and-off'),
        ],className="card"),
        html.Div(children=[
            html.Img(id='fan', src=LED_OFF),
            html.Button(children='Switch', n_clicks=0, id='fan-on-and-off'),
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
    print('light click')
    if click:
        # GPIO.output(LED, GPIO.HIGH)
        return [LED_ON,'toggleOn']
    else:
        # GPIO.output(LED, GPIO.LOW)
        return [LED_OFF,'toggleOff']
    
@app.callback(
    #adding an array means the input or output must contain an array
    Output('button-send-email', 'className'),
    Input('button-send-email', 'n_clicks')
)
def sendEmail(n_clicks):
    if n_clicks == 0: return
    print('email click')
    try:
        # Connect to the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Connected to server")
        
        # Send the actual email
        print()
        print(f"Sending email to - {email_to}")
        TIE_server.sendmail(email_from, email_to, message)
        print(f"Email successfully sent to - {email_to}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()
    receiveEmail()
    return 'sent'

def receiveEmail():
    return

@app.callback(
        [Output('fan', 'src'),Output('fan-on-and-off', 'className')],
        Input('fan-on-and-off', 'n_clicks')
)
def update_FAN(n_clicks):
    click = n_clicks % 2
    print('fan click')
    if click:
        # GPIO.output(LED, GPIO.HIGH)
        return [LED_ON,'toggleOn']
    else:
        # GPIO.output(LED, GPIO.LOW)
        return [LED_OFF,'toggleOff']

if __name__ == '__main__':
    # this is a theory but
    # if you write your ip from another device and port X.X.X.X:8050 on a browser 
    # you can connect to the website from that device
    # app.run(host='0.0.0.0',debug=True)
    # this is if you want to run it on your current device
    app.run(debug=True)