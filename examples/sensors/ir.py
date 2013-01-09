import time
import sys
sys.path.append("../..")

import arduino

# Example code to run an IR sensor. Turns on the LED
# at digital pin 13 when the IR sensor detects anything within
# a certain distance.

THRESH = 200.0  # Experimentally chosen

ard = arduino.Arduino()  # Create the Arduino object
a1 = arduino.AnalogInput(ard, 1)
a2 = arduino.AnalogInput(ard, 2)
a3 = arduino.AnalogInput(ard, 5)
ard.run()  # Start the thread which communicates with the Arduino

# Main loop -- check the sensor and update the digital output
while True:
    print str(a1.getValue()) + " " + str(a2.getValue()) + " " + str(a3.getValue()) 
    time.sleep(0.1)
