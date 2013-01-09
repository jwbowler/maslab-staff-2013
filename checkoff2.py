import time
import sys

import arduino

# Example code to run an IR sensor. Turns on the LED
# at digital pin 13 when the IR sensor detects anything within
# a certain distance.

THRESH = 220.0  # Experimentally chosen

ard = arduino.Arduino()  # Create the Arduino object
a0 = arduino.AnalogInput(ard, 1)  # Create an analog sensor on pin A0
m0 = arduino.Motor(ard, 10, 5, 3)
m1 = arduino.Motor(ard, 10, 6, 4)
ard.run()  # Start the thread which communicates with the Arduino

while True:
    speed = -127
    
    m0.setSpeed(speed)
    m1.setSpeed(speed)

    # Main loop -- check the sensor and update the digital output
    while True:
        ir_val = a0.getValue() # Note -- the higher value, the *closer* the dist
        print ir_val, ir_val >= THRESH
        if ir_val >= THRESH:
            break
        time.sleep(0.1)

    m0.setSpeed(0)
    m1.setSpeed(-speed)
    time.sleep(2)
