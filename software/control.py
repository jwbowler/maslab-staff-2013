import arduino
import pid

log = False

class Control:
    def __init__(self, ard):
        self.ard = ard

        self.motors = [ \
                        arduino.Motor(ard, 10, 5, 6),  \
                        arduino.Motor(ard, 10, 9, 10), \
                        arduino.Motor(ard, 10, 3, 4)   \
                      ]
    
    def drive(self, r, l):
        if log:
            print "DRIVE: r=" + str(r) + ", l=" + str(l)
        self.motors[0].setSpeed(-r)
        self.motors[1].setSpeed(-l)

    def setBallCapture(self, run):
        self.motors[2].setSpeed(0)
        
    def ballCaptureOn(self):
        if log:
            print "CAPTURE MOTOR ON"
        self.motors[2].setSpeed(-127)
        
    def ballCaptureOff(self):
        if log:
            print "CAPTURE MOTOR OFF"
        self.motors[2].setSpeed(0)
        

class ControlDummy:
    
    def __init__(self, ard):
        pass
        
    def drive(self, r, l):
        if log:
            print "DRIVE: r=" + str(r) + ", l=" + str(l)
            
    def ballCaptureOn(self):
        if log:
            print "CAPTURE MOTOR ON"
        
    def ballCaptureOff(self):
        if log:
            print "CAPTURE MOTOR OFF"
