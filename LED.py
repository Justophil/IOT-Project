import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class LED:
    def __init__(self, pin,pinr):
        self.pin = pin
        self.pinr = pinr
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pinr, GPIO.OUT, initial=GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def turnR_on(self):
        GPIO.output(self.pinr, GPIO.HIGH)

    def turnR_off(self):
        GPIO.output(self.pinr, GPIO.LOW)