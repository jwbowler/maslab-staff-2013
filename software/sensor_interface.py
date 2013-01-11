import arduino

class SensorInterface:

	def __init__(self, arduino):
        self.ard = arduino

        # (arduino pin, angle, radial distance from robot center)
        self.irList = [(0,-90,1), (1,-45,1), (2,0,1), (3,45,1), (4,90,1)]    

        self.irRefs = [arduino.AnalogInput(self.ard, i[0]) \
                        for i in self.irList]
        
    # Returns list of (sighted feature type, (distance, angle))
    def get(self):
        return [("IR", (convert(self.irRefs[i].getValue) + self.irList[i][2], \
                self.irList[i][1])) for i in range(self.irList)]
        
        def convert(irReading):
            #TODO
            pass
    
    
            
