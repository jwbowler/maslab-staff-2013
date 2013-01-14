import utils
import pid
import time

class HuntBallAction():

    def __init__(self, control):
        self.ctl = control
        self.rotationSpeed = .3
        self.targetSpeed = .3
        self.myPid = pid.Pid(.03,.005,.005,100)
        
    def getName(self):
        return "ACTION_HUNT_BALL"

    def step(self, (distance, angle)):
        angle = -angle

        if (not self.myPid.running):
            self.myPid.start(angle, 0)

        pidVal = self.myPid.iterate(angle)

        adjustedSpeed = self.targetSpeed * ((90.0-abs(angle))/90.0)

        (r, l) = utils.getMotorSpeeds(adjustedSpeed, self.rotationSpeed * pidVal)

        r = int(utils.boundAndScale(r, 0, 1.0, .01, 8, 127))
        l = int(utils.boundAndScale(l, 0, 1.0, .01, 8, 127))

        self.ctl.drive(r, l)
