from vision import balltrackingscript

log = True

class VisionInterface:

    def __init__(self):
        self.bt = balltrackingscript.BallTracker()
        self.bt.start()
    
    # Returns list of (sighted object type, (x pos on screen, y pos on screen))
    def get(self):
        self.bt.update()
        self.frameID = self.bt.getFrameID()
        out = [(self.bt.getType(i), (self.bt.getX(i), self.bt.getY(i)), self.bt.getWeight(i)) \
            for i in range(self.bt.getNumObj())]
        if log:
            print "FRAME " + str(self.frameID)
            print "VISION DATA:"
            print out
        return out
        
    def __del__(self):
        self.bt.stop()
        


class VisionInterfaceDummy:

    def __init__(self):
        pass

    def get(self):
        return [("RED_BALL", (100, 400), 50), ("GREEN_BALL", (200, 300), 60)]
        if log:
            print "MOCK VISION DATA:"
            print out
        return out
    
