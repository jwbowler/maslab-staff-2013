import time
import utils

class Pid:

    #creates a new pid loop
    #kp, ki, kd are self explanatory
    #pid output is capped to oLim
    #accumulated i is capped to iLim (before ki is applied)
    #dTime is the time over which the d component is calculated
    def __init__(self, kp, ki, kd, oLim, iLim, dTime = .05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.iLim = iLim
        self.oLim = oLim
        self.dTime = dTime

        self.prevOut = None

        self.prevValue = None
        self.prevTime = None
        self.pastVals = []
        self.running = False

    def start(self, value, target):
        self.i = 0
        self.target = target
        self.prevVals = []
        self.prevValue = value
        self.prevTime = time.time()
        self.running = True
        self.pastVals.append((self.prevTime, self.prevValue))

    def stop(self):
        self.running = False
 
    def iterate(self, value):
        curTime = time.time()
        dt = curTime - self.prevTime 

        self.prevVals.append((curTime, value))
        for i in xrange(len(self.prevVals)):
            if self.prevVals[i][0] + self.dTime > curTime:
                self.prevVals = self.prevVals[i:]
                break

        longDt = self.prevVals[-1][0]-self.prevVals[0][0]
        longDx = self.prevVals[-1][1]-self.prevVals[0][1]

        p = self.target-value
        d = 0 if longDt == 0 else (longDx/longDt)
        self.i += p*dt;

        self.i = utils.absBound(self.i, self.iLim)

        out = p*self.kp + d*self.kd + self.i*self.ki
        out = utils.absBound(out, self.oLim)

        self.prevTime = curTime
        self.prevValue = value
        self.prevOut = out
        
        return out
    
    def getLastOutput(self):
        return self.prevOut
