import utils
import pid
import time

class HuntBallState():

    def __init__(self, control):
    
        self.ctl = control
        self.rotationSpeed = .2
        self.targetSpeed = .1
        self.myPid = pid.Pid(.03,.005,.005,100)
        
    def getStateName(self):
        return "HUNT_BALL"

    def step(self, data):
    
        (r, l) = (0, 0)

        objTypes = [i[0] for i in data]
        if not ("RED_BALL" in objTypes or "GREEN_BALL" in objTypes):
            return (None, "FOLLOW_WALL")
        if "RED_BALL" in objTypes:
            i = objTypes.index("RED_BALL")
        else:
            i = objTypes.index("GREEN_BALL")
        
        (ballType, (distance, angle)) = data[i]
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
        
        return (None, self.getStateName())
        
    '''
    def nextState(self, data):
        objTypes = [i[0] for i in data]
        if not ("RED_BALL" in objTypes or "GREEN_BALL" in objTypes):
            return "FOLLOW_WALL"
        else:
            return self.getStateName()
    '''
   
