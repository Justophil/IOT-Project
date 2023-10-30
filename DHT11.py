import Freenove_DHT as DHT

class DHT11:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        dht = DHT.DHT(self.pin) #create a DHT class object
        chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether  data read is normal according to the return value.
        if (chk is not dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            pass
        return [dht.temperature,dht.humidity]
        # pass # only without the GPIO output