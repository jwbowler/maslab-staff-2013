import time
import sys
import pid
import utils
import arduino

class FollowWallState():

    #TODO: get it to use state information instead of arduino input
    def __init__(self, ard, control):
        self.ctl = control
        
        self.a1 = arduino.AnalogInput(ard, 1)  # Create an analog sensor on pin A1
        self.a2 = arduino.AnalogInput(ard, 2)  # Create an analog sensor on pin A2
        self.a3 = arduino.AnalogInput(ard, 7)  # Create an analog sensor on pin A3

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
       # Main loop -- check the sensor and update the digital output\
        ir_val = [self.a1.getValue(), self.a2.getValue(), self.a3.getValue()] # Note -- the higher value, the *closer* the dist
        for i in xrange(3):
              print "IR #" + str(i)+ " " +str(ir_val[i])+ " " + str(ir_val[i]<=self.THRESH[i])

        if ir_val[0]!=None and  ir_val [1]!= None and ir_val[2]!=None:
            ir_val = [self.a1.getValue(), self.a2.getValue(), self.a3.getValue()] # Note -- the higher value, the *closer* the dist
            if (not self.IRPid[0].running):
                self.IRPid1.start(ir_val[0], self.THRESH[0])
                self.IRPid2.start(ir_val[1], self.THRESH[1])
                self.IRPid3.start(ir_val[2], self.THRESH[2])

            self.PidOut[0]=self.IRPid1.iterate(ir_val[0])
            self.PidOut[1]=self.IRPid2.iterate(ir_val[1])
            self.PidOut[2]=self.IRPid3.iterate(ir_val[2])

            (r,l)=utils.getMotorSpeeds(Speed,sum(self.PidOut[1:])*self.RotationSpeed)

            rSpeed = -int(utils.boundAndScale(r, 0, 1.0, .01, 8, 127))
            lSpeed = -int(utils.boundAndScale(l, 0, 1.0, .01, 8, 127))

            ctl.drive(rSpeed, lSpeed)
            print (ir_val, (rSpeed, lSpeed))
            print (self.PidOut, sum(self.PidOut[1:])*self.RotationSpeed)
            
        return (None, self.nextState(data))
              
    def nextState(self, data):
        objTypes = [i[0] for i in data]
        if "RED_BALL" in objTypes or "GREEN_BALL" in objTypes:
            return "HUNT_BALL"
        else:
            return self.getStateName()
