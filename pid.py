import time;

class Pid:

  (kp, ki, kd, iLim) = (0,0,0,0)
  (i, target, prevValue, prevTime) = (0,0,0,0)

  def __init__(self, p, i, d, lim):
    self.kp = p
    self.ki = i
    self.kd = d
    self.iLim = lim;

  def start(self, value, target):
    self.i = 0
    self.prevValue = value
    self.prevTime = time.time()
 
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

    return (p*self.kp + d*self.kd + self.i*self.ki)

if __name__ == '__main__':
  myPid = Pid(.1,.05,.05,100)

  v = 100
  myPid.start(0, v)

  while(True):
    o = myPid.iterate(v)
    v += o
    print (v, o)
    time.sleep(.1)
  
  
