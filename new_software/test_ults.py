import time
import sys
import arduino

ard = arduino.Arduino()
ult = arduino.Ult(ard,14,15)
ard.run()

while True:
  print str(ult.getRawValues())
  time.sleep(0.1)
