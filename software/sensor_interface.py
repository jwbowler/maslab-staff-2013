import arduino

log = False

class SensorInterface:

    def __init__(self, ard):
        self.ard = ard

        # (arduino pin, angle, radial distance from robot center)
        self.irList = [(0,-90,1), (1,-45,1), (2,0,1), (3,45,1), (4,90,1)]    

        self.irRefs = [arduino.AnalogInput(self.ard, i[0]) \
                        for i in self.irList]
        
    # Returns list of (sighted feature type, (distance, angle))
    def get(self):
    
        def convert(irReading):
            #TODO
            return irReading;
        
        out = [("IR", (convert(self.irRefs[i].getValue()) + self.irList[i][2], \
                self.irList[i][1])) for i in range(len(self.irList))]
        if log:
            print "SENSOR DATA:"
            print out
        return out


class SensorInterfaceDummy:

    def __init__(self, ard):
        pass
        
    def get(self):
        out =  [("IR", (10, -45)), ("IR", (20, 0)), ("IR", (30, 45))]
        if log:
            print "MOCK SENSOR DATA:"
            print out
        return out
    
            
