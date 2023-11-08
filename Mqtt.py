import paho.mqtt.client as mqtt

class Mqtt:
    client_id = "" # client id for connecting, if length = 0 or None it creates a new one if clean_session is true
    clean_session=True
    userdata=None
    protocol='MQTTv311'
    transport='tcp'
    client = mqtt.Client(client_id=client_id,clean_session=clean_session,userdata=userdata,protocol=protocol,transport=transport)
    
    def connect():
        mqtt.connect("mqtt.eclipseprojects.io") # if no raspberry pi
        # mqtt.connect("0.0.0.0") # if raspberry pi (needs ip of raspberry pi)