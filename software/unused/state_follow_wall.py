import time
import sys
import pid
import utils
import arduino

log = True

class FollowWallState():

    #TODO: get it to use state information instead of arduino input
    def __init__(self, control):
        
        self.ctl = control
       
        self.IRPid1= pid.Pid(0.000, 0.000, 0.000, 50)
        self.IRPid2= pid.Pid(0.004, 0.000, 0.000, 100)
        self.IRPid3= pid.Pid(.002, 0.000, 0.000, 50)
        self.IRPid=[self.IRPid1, self.IRPid2, self.IRPid3]

        self.THRESH=[200, 250, 410]

        self.PidOut=[0,0,0]

        self.Speed=.2
        self.RotationSpeed=.2
        
    def getStateName(self):
        return "FOLLOW_WALL"

    def step(self, data):
        
        ir_data = [obj[1] for obj in data if obj[0] == "IR"]
        ir_val = [ir_data[0][0], ir_data[1][0], ir_data[2][0]]
        if log:
            for i in xrange(3):
                print "IR #" + str(i)+ " " +str(ir_val[i])+ " " + str(ir_val[i]<=self.THRESH[i])

        if ir_val[0] != None and ir_val[1] != None and ir_val[2] != None:
            if (not self.IRPid[0].running):
                self.IRPid1.start(ir_val[0], self.THRESH[0])
                self.IRPid2.start(ir_val[1], self.THRESH[1])
                self.IRPid3.start(ir_val[2], self.THRESH[2])

            self.PidOut[0]=self.IRPid1.iterate(ir_val[0])
            self.PidOut[1]=self.IRPid2.iterate(ir_val[1])
            self.PidOut[2]=self.IRPid3.iterate(ir_val[2])

            (r,l)=utils.getMotorSpeeds(self.Speed,sum(self.PidOut[1:])*self.RotationSpeed)

            rSpeed = -int(utils.boundAndScale(r, 0, 1.0, .01, 8, 127))
            lSpeed = -int(utils.boundAndScale(l, 0, 1.0, .01, 8, 127))
            
            if log:
                print (ir_val, (rSpeed, lSpeed))
                print (self.PidOut, sum(self.PidOut[1:])*self.RotationSpeed)
            self.ctl.drive(rSpeed, lSpeed)
            
        return (None, self.nextState(data))

        '''
        self.ctl.drive(0, 0)
        return (None, self.nextState(data))
        '''
              
    def nextState(self, data):
        objTypes = [i[0] for i in data]
        if "RED_BALL" in objTypes or "GREEN_BALL" in objTypes:
            return "HUNT_BALL"
        else:
            return self.getStateName()
