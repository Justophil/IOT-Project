import paho.mqtt.client as mqtt

class Mqtt:
    client_id = "" # client id for connecting, if length = 0 or None it creates a new one if clean_session is true
    clean_session=True
    server="192.168.0.144"
    # server="mqtt.eclipseprojects.io"
    username=''
    password=''
    client = None
    data=[]
    topic="LightIntensity"

    def __init__(self, username = 'username', password = 'pass'):
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id=self.client_id,clean_session=self.clean_session)
        self.client.username_pw_set(self.username, self.password)
    
    def on_message(message):
        global data
        data['light'] = int(message.payload.decode("utf-8"))

    def on_connect():
        global subscribe
        subscribe()

    def connect(self):
        self.client.connect(self.server)
        self.client.on_message = self.on_message

    def subscribe(self):
        self.client.subscribe(self.topic)

    # def publish(self):
        # self.client.publish()

    