import sys
sys.path.append("../..")
import time

import arduino

ard = arduino.Arduino()
m0 = arduino.Motor(ard, 0, 2, 3)
m1 = arduino.Motor(ard, 0, 2, 4)
led = arduino.DigitalOutput(ard, 13)
ard.run()  # Start the Arduino communication thread

while True:
    led.setValue(1)
    m0.setSpeed(100)
    m1.setSpeed(100)
    time.sleep(1)
    led.setValue(0)
    m0.setSpeed(0)
    m1.setSpeed(0)
    time.sleep(1)
    led.setValue(1)
    m0.setSpeed(-100)
    m1.setSpeed(-100)
    time.sleep(1)
    led.setValue(0)
    m0.setSpeed(0)
    m1.setSpeed(0)
    time.sleep(1)
