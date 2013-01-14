class RotateInPlaceAction():

    def __init__(self, control):
    
        self.ctl = control
        
    def getName(self):
        return "ACTION_ROTATE_IN_PLACE"

    def step(self):

        self.ctl.drive(30, -30)
        
