import math

class DataCollection:

    def __init__(self, visionInterface, sensorInterface):
        self.vi = visionInterface
        self.si = sensorInterface
        self.cam = Camera()

    # Returns list of (sighted feature type, distance, angle)
    def get(self):
    
        def getPolarFromScreen((x, y)):
            cam = self.cam
            angle2obj = (cam.angle + cam.vfov/2 - cam.vfov*(1.0 * y / cam.imHeight))
            d = cam.elev * math.tan((math.pi/180) * angle2obj)
            if d < 0:
                d = math.isInf()
            a = (x - (cam.imHeight/2.)) * cam.hfov / cam.imWidth
            return (d, a)
            
        visionDataRaw = self.vi.get()
        print "VISION DATA RAW:"
        print visionDataRaw
        visionData = [(t, getPolarFromScreen(loc)) for (t, loc) in visionDataRaw]
        sensorData = self.si.get()
        return visionData + sensorData
                    
        
class Camera:
    def __init__(self):
        self.elev = 0.1
        self.angle = 60. # 0 == pointing down; 90 = pointing forward
        self.imWidth = 640
        self.imHeight = 480
        self.ar = 1. * self.imWidth / self.imHeight
        self.vfov = 50.
        self.hfov = self.ar * self.vfov
            

