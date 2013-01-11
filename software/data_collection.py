import math

class DataCollection:

    def __init__(self, visionWrapper, sensorWrapper):
        self.vw = visionWrapper
        self.sw = sensorWrapper
        self.cam = Camera()

    # Returns list of (sighted feature type, distance, angle)
    def get():
        visionDataRaw = self.vw.get()
        visionData = [(t, getPolarFromScreen(loc)) for (t, loc) in visionDataRaw]
        sensorData = self.sw.get()
        return visionData.extend(sensorData)
        
        def getPolarFromScreen((x, y)):
            d = cam.imHeight * tan(cam.angle - cam.vfov/2 + cam.vfov*(y / cam.imHeight))
            if d < 0:
                d = math.isInf()
            a = (x - (cam.imHeight/2.)) * cam.hfov / cam.imWidth
            
        
class Camera:
    def __init__(self):
        self.elev = 1.
        self.angle = 60. # 0 == pointing forward; 90 = pointing down
        self.imWidth = 640
        self.imHeight = 480
        self.ar = 1. * self.width / self.height
        self.vfov = 50.
        self.hfov = self.ar * self.vfov
            

