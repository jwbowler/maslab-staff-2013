import utils
import pid
import time

from vision import balltrackingscript

import arduino

bt = balltrackingscript.BallTracker()

def main():

  global bt
  global mRight
  global mLeft

  #vision
  camAngle = 0
  camHeight = 6
  camXFov = 67
  camYFov = 50
  imageHeight = 480
  imageWidth = 640

  #arduino
  ard = arduino.Arduino()
  mRight = arduino.Motor(ard, 10, 5, 3)
  mLeft = arduino.Motor(ard, 10, 6, 4)
  ard.run()

  #motion
  rotationSpeed = .2
  targetSpeed = .1
  
  #pid
  myPid = pid.Pid(.03,.005,.005,100)

  #state
  searchState = 0
  huntState = 1
  doneState = 2

  state = 0

  bt.start()
  
  #fps
  tLast = time.time()
  tAvg = 0

  while True:
    (r, l) = (0, 0)
    loc = bt.update()

    if state == searchState:
      print "search"

      (r, l) = utils.getMotorSpeeds(0.0, rotationSpeed)

      if (loc != 0):
        state = huntState

    if state == huntState:
      print "hunt"

      y = loc % imageHeight
      x = loc / imageHeight
      print (x, y)

      distance = 0
      angle = (x - (imageHeight/2.0)) * camXFov / imageWidth
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
        #state = doneState

    print (r, l)
    r = int(utils.boundAndScale(r, 0, 1.0, .01, 16, 127))
    l = int(utils.boundAndScale(l, 0, 1.0, .01, 16, 127))
    print (r, l)

    mRight.setSpeed(-r)
    mLeft.setSpeed(-l)
    
    tCurr = time.time()
    tDiff = tCurr - tLast
    tLast = tCurr
    tAvg = 0.9*tAvg + 0.1*tDiff
    print 1/tAvg
    
def stopRobot():
  global mRight
  global mLeft
  mRight.setSpeed(0)
  mLeft.setSpeed(0)
   
