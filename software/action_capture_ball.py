class CaptureBallAction():

    def __init__(self, control):
    
        self.ctl = control
        
    def getName(self):
        return "ACTION_CAPTURE_BALL"

    def step(self, bLastStep):

        self.ctl.drive(100, 100)
        if not bLastStep:
            self.ctl.ballCaptureOff()
        else:
            self.ctl.ballCaptureOn()
