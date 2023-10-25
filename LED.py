# import RPi.GPIO as GPIO

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering

class LED:
    def __init__(self, pin):
        self.pin = pin
        # GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def turn_on(self):
        # GPIO.output(self.pin, GPIO.HIGH)
        print('on')

    def turn_off(self):
        # GPIO.output(self.pin, GPIO.LOW)
        print('off')