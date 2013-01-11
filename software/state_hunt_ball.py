import utils
import pid
import time

class HuntBallState():

    def __init__(control):
    
        self.ctl = control
        self.rotationSpeed = .2
        self.targetSpeed = .1
        self.myPid = pid.Pid(.03,.005,.005,100)

    def step(data):
    
        (r, l) = (0, 0)

        objTypes = [i[0] for i in data]
        if not ("RED_BALL" in objTypes or "GREEN_BALL" in objTypes):
            return (None, "WALL_FOLLOW")
        if "RED_BALL" in objTypes:
            i = objTypes.index("RED_BALL")
        else:
            i = objTypes.index("GREEN_BALL")
        
        (ballType, distance, angle) = data[i]
        print angle

        if (not myPid.running):
            myPid.start(angle, 0)
            continue

        print 'running'
  
        pidVal = myPid.iterate(angle)

        print pidVal

        (r, l) = utils.getMotorSpeeds(targetSpeed, rotationSpeed * pidVal)

        if (loc != None):
            pass

        print (r, l)
        r = int(utils.boundAndScale(r, 0, 1.0, .01, 16, 127))
        l = int(utils.boundAndScale(l, 0, 1.0, .01, 16, 127))
        print (r, l)

        ctl.drive(r, l)
        
        
    def nextState(data):
        objTypes = [i[0] for i in data]
        if "RED_BALL" in objTypes or "GREEN_BALL" in objTypes:
            return "HUNT_BALL"
        else:
            return self.getStateName()
   
