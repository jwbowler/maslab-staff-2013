class CaptureBallAction():
    def __init__(self, control):
        self.ctl = control
        
    def getName(self):
        return "ACTION_CAPTURE_BALL"

    def step(self, runRoller):
        self.ctl.drive(32, 32)
        if not runRoller:
            self.ctl.ballCaptureOff()
        else:
            self.ctl.ballCaptureOn()
