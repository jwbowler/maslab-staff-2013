import commander as c
import time
import arduino
from config import *

class Start():

    def __init__(self):
        self.colorSwitch = arduino.DigitalInput(c.ARD(), COLOR_SWITCH_PIN)
        self.resetButton = arduino.DigitalInput(c.ARD(), RESET_BUTTON_PIN)

    def poll(self):
        #return True
        if self.resetButton.getValue():
            if self.colorSwitch.getValue():
                return True
            else:
                return False
        else:
            return None
