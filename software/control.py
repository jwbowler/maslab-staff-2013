import arduino
import pid

class Control:
    def __init__(self, ard):
        self.ard = ard

        self.motors = [ \
                        arduino.Motor(ard, 10, 5, 3), \
                        arduino.Motor(ard, 10, 6, 4)  \
                      ]
    
    def drive(self, r, l):
        print "DRIVE: r=" + str(r) + ", l=" + str(l)
        self.motors[0].setSpeed(-r)
        self.motors[1].setSpeed(-l)
        
    def ballCaptureOn(self):
        pass
        
    def ballCaptureOff(self):
        pass
        

class ControlDummy:
    
    def __init__(self, ard):
        pass
        
    def drive(self, r, l):
        print "DRIVE: r=" + str(r) + ", l=" + str(l)
