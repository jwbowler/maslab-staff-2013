import time
import sys
import pid
import arduino
import utils

ard = arduino.Arduino()  # Create the Arduino object
a1 = arduino.AnalogInput(ard, 1)  # Create an analog sensor on pin A1
a2 = arduino.AnalogInput(ard, 2)  # Create an analog sensor on pin A2
a3 = arduino.AnalogInput(ard, 3)  # Create an analog sensor on pin A3
m0 = arduino.Motor(ard, 10, 5, 3)
m1 = arduino.Motor(ard, 10, 6, 4)
ard.run()  # Start the thread which communicates with the Arduino

IRPid1= pid.Pid()
IRPid2= pid.Pid()
IRPid3= pid.Pid()
IRPid=[IRPid1,IRPid2,IRPid3]

TRESH=[0,0,0]

PidOut=[0,0,0]

Speed=80
while True:
    # Main loop -- check the sensor and update the digital output
    while True:
        ir_val = [a0.getValue(),a1.getValue(),a2.getValue()] # Note -- the higher value, the *closer* the dist
        for i in xrange(3):
          PidOut[i] IRPid[i].iterate(ir_val[i])
          print "IR #" + str(i) + ir_val[i], irval[i]<=TRESH[i]
        
        (r,l)=utils.getMotorSpeeds(Speed,sum(PidOut))
        rSpeed= int(boundAndScale(r, 0, 1.0, .01, 16, 127))
        lSpeed = int(boundAndScale(l, 0, 1.0, .01, 16, 127))
        m0.setSpeed(rSpeed)
        m1.setSpeed(lSpeed)
