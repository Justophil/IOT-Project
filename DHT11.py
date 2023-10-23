# import RPi.GPIO as GPIO
# import Freenove_DHT as DHT
import time as sleep

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)

class DHT11:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        # dht = DHT.DHT(self.pin) #create a DHT class object
        # chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether  data read is normal according to the return value.
        # if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            # break
        # else:
            # return
        # return [dht.temperature,dht.humidity]
        print('DHT11 Test')