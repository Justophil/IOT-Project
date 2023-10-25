# import RPi.GPIO as GPIO

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering

class DCMotor:
    def __init__(self, enable,input1,input2):
        self.enable = enable
        self.input1 = input1
        self.input2 = input2
        # GPIO.setup(enable, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(input1, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(input2, GPIO.OUT, initial=GPIO.LOW)

    # methods for turning on and off here
    def turn_on(self):
        # GPIO.output(self.enable, 1)
        # GPIO.output(self.input1, 0)
        # GPIO.output(self.input2, 1)

        # GPIO.output(self.enable, 1)
        # GPIO.output(self.input1, 1)
        # GPIO.output(self.input2, 0)
        pass

    def turn_off(self):
        # GPIO.output(self.enable, 1)
        # GPIO.output(self.input1, 1)
        # GPIO.output(self.input2, 1)

        # GPIO.output(self.enable, 1)
        # GPIO.output(self.input1, 0)
        # GPIO.output(self.input2, 0)
        pass