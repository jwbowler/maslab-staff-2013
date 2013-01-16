class RotateInPlaceAction():
    def __init__(self, control):
        self.ctl = control
        
    def getName(self):
        return "ACTION_ROTATE_IN_PLACE"

    def step(self, dir):
        self.ctl.drive(48*dir, -48*dir)
