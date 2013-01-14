class EmergencyReverseAction():

    def __init__(self, control):
    
        self.ctl = control
        
    def getName(self):
        return "ACTION_EMERGENCY_REVERSE"

    def step(self):

        self.ctl.drive(-100, -100)
        
