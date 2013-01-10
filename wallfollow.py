import time
import sys
import pid
import arduino
import utils

ard = arduino.Arduino()  # Create the Arduino object
a1 = arduino.AnalogInput(ard, 1)  # Create an analog sensor on pin A1
a2 = arduino.AnalogInput(ard, 2)  # Create an analog sensor on pin A2
a3 = arduino.AnalogInput(ard, 7)  # Create an analog sensor on pin A3
m0 = arduino.Motor(ard, 10, 5, 3)
m1 = arduino.Motor(ard, 10, 6, 4)
ard.run()  # Start the thread which communicates with the Arduino

IRPid1= pid.Pid(0.000, 0.000, 0.000, 50)
IRPid2= pid.Pid(0.004, 0.000, 0.000, 100)
IRPid3= pid.Pid(.002, 0.000, 0.000, 50)
IRPid=[IRPid1,IRPid2,IRPid3]

THRESH=[200, 250, 410]

PidOut=[0,0,0]

Speed=.2
RotationSpeed=.2


while True:
   # Main loop -- check the sensor and update the digital output\
    ir_val = [a1.getValue(),a2.getValue(),a3.getValue()] # Note -- the higher value, the *closer* the dist
    for i in xrange(3):
          print "IR #" + str(i)+ " " +str(ir_val[i])+ " " + str(ir_val[i]<=THRESH[i])

    while ir_val[0]!=None and  ir_val [1]!= None and ir_val[2]!=None:
        ir_val = [a1.getValue(),a2.getValue(),a3.getValue()] # Note -- the higher value, the *closer* the dist
        if (not IRPid[0].running):
            IRPid1.start(ir_val[0],THRESH[0])
            IRPid2.start(ir_val[1],THRESH[1])
            IRPid3.start(ir_val[2],THRESH[2])

        PidOut[0]=IRPid1.iterate(ir_val[0])
        PidOut[1]=IRPid2.iterate(ir_val[1])
        PidOut[2]=IRPid3.iterate(ir_val[2])

        (r,l)=utils.getMotorSpeeds(Speed,sum(PidOut[1:])*RotationSpeed)

        rSpeed = -int(utils.boundAndScale(r, 0, 1.0, .01, 8, 127))
        lSpeed = -int(utils.boundAndScale(l, 0, 1.0, .01, 8, 127))

        m0.setSpeed(rSpeed)
        m1.setSpeed(lSpeed)
        print (ir_val, (rSpeed, lSpeed))
        print (PidOut, sum(PidOut[1:])*RotationSpeed)
        time.sleep(0.1)
