from dash import Dash, html, callback, Output, Input
# import RPi.GPIO as GPIO
# import time as sleep

app = Dash(__name__)

IMG_ON = '/assets/img/on.png'
IMG_OFF = '/assets/img/off.png'
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED=17
# GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

app.layout = html.Div([
    html.Div(children=[
        html.H1('Dashboard'),
        html.Img(id='bulb', src=IMG_OFF),
        html.Br(),
        html.Button(children='Switch', n_clicks=0, id='button-on-and-off')          
        ]),
])
@callback(
    [Output('bulb', 'src')],
    Input('button-on-and-off', 'n_clicks')
)
def update_LED (n_clicks):
    click = n_clicks % 2
    if click:
        # GPIO.output(LED, GPIO.HIGH)
        return IMG_ON 
    else:
        # GPIO.output(LED, GPIO.LOW)
        return IMG_OFF

if __name__ == '__main__':
    app.run(debug=True)