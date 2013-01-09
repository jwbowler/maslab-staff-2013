import utils
import pid

from vision import balltrackingscript

import arduino

#vision
camAngle = 0
camHeight = 6
camXFov = 67
camYFov = 50
imageHeight = 480
imageWidth = 640

balltrackingscript.setup()

#arduino
ard = arduino.Arduino()
mRight = arduino.Motor(ard, 10, 5, 3)
mLeft = arduino.Motor(ard, 10, 6, 4)

#motion
rotationSpeed = .2
targetSpeed = .2


#pid
myPid = pid.Pid(1,0,0,0)

#state
searchState = 0
huntState = 1
doneState = 2

state = 0

while True:
  (r, l) = (0, 0)
  loc = balltrackingscript.run()

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

    if (not myPid.running):
      myPid.start(angle, 0)
      continue
    
    pidVal = myPid.iterate(angle)

    (r, l) = utils.getMotorSpeeds(targetSpeed, rotationSpeed * pidVal)

    if (loc != None):
      pass
      #state = doneState

  r = int(utils.boundAndScale(r, 0, 1.0, .01, 32, 255)/2)
  l = int(utils.boundAndScale(l, 0, 1.0, .01, 32, 255)/2)
  mRight.setSpeed(r)
  mLeft.setSpeed(l)
