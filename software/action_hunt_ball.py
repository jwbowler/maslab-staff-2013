import utils
import pid
import time

class HuntBallAction():

    def __init__(self, control):
    
        self.ctl = control
        self.rotationSpeed = .2
        self.targetSpeed = .1
        self.myPid = pid.Pid(.03,.005,.005,100)
        
    def getName(self):
        return "ACTION_HUNT_BALL"

    def step(self, (distance, angle)):
    
        (r, l) = (0, 0)
        
        angle = -angle #this shouldn't be necessary...
        #print angle

        if (not self.myPid.running):
            self.myPid.start(angle, 0)

        #print 'running'
  
        pidVal = self.myPid.iterate(angle)

        #print pidVal

        (r, l) = utils.getMotorSpeeds(self.targetSpeed, self.rotationSpeed * pidVal)

        #print (r, l)
        r = int(utils.boundAndScale(r, 0, 1.0, .01, 16, 127))
        l = int(utils.boundAndScale(l, 0, 1.0, .01, 16, 127))
        #print (r, l)

        self.ctl.drive(r, l)
   
