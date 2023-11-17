import paho.mqtt.client as mqtt
import threading

class Mqtt:
    client_id = "" # client id for connecting, if length = 0 or None it creates a new one if clean_session is true
    clean_session=True
    # server="192.168.0.144"
    server="172.20.10.3"
    data=0
    topic="LightIntensity"
    topic="RFID"

    def __init__(self, username = 'username', password = 'pass'):
        self.username = username
        self.password = password
        
        self.client = mqtt.Client()
        # self.client.connect(Mqtt.server)
        # self.client.connect("localhost")

        # self.client.on_connect = Mqtt.on_connect
        # self.client.on_message = Mqtt.on_message
        self.setup()
        # self.client.username_pw_set(self.username, self.password)
    
    def on_message(client, userdata, message):
        Mqtt.data = int(message.payload.decode("utf-8"))

    def on_connect(client, userdata, flags, rc):
        client.subscribe(Mqtt.topic)

    def run(self):
        thread = threading.Thread(target=self.client.loop_start())
        thread.daemon = True
        thread.start()

    # def subscribe(self):
    #     self.client.subscribe(Mqtt.topic)

    # def publish(self):
        # self.client.publish()
    def setup(self):
        self.client.connect(Mqtt.server)

        self.client.on_connect = Mqtt.on_connect
        self.client.on_message = Mqtt.on_message
    