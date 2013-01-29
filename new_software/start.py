import time
import arduino
import commander as c
from config import *

class Start():

    def __init__(self):
        self.colorSwitch = arduino.DigitalInput(c.ARD(), COLOR_SWITCH_PIN)
        self.resetButton = arduino.DigitalInput(c.ARD(), RESET_BUTTON_PIN)

    def poll(self):
        if self.resetButton.getValue():
            print self.colorSwitch.getValue()
            if self.colorSwitch.getValue():
                return True
            else:
                return False
        else:
            return None
