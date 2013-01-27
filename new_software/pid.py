import time;

class Pid:

    (kp, ki, kd, iLim) = (0,0,0,0)
    (i, target, prevValue, prevTime) = (0,0,0,0)
    running = False

    def __init__(self, p, i, d, oLim, iLim):
        self.kp = p
        self.ki = i
        self.kd = d
        self.iLim = iLim
        self.oLim = oLim

    def start(self, value, target):
        self.i = 0
        self.target = target
        self.prevValue = value
        self.prevTime = time.time()
        self.running = True

    def stop(self):
        self.running = False
 
    def iterate(self, value):
        curTime = time.time()
        dt = curTime - self.prevTime 
        dx = value - self.prevValue

        p = self.target-value
        d = 0 if dt == 0 else (dx/dt)
        self.i += p*dt;

        if self.i > self.iLim:
            self.i = self.iLim
        elif -self.i > self.iLim:
            self.i = -self.iLim

        self.prevTime = curTime
        self.prevValue = value

        out = p*self.kp + d*self.kd + self.i*self.ki
        if out > self.oLim:
            return self.oLim
        elif out < -self.oLim:
            return -self.oLim

        return out
