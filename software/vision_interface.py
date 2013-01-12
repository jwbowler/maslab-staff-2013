from vision import balltrackingscript

class VisionInterface:

    def __init__(self):
        self.bt = balltrackingscript.BallTracker()
        self.bt.start()
    
    # Returns list of (sighted object type, (x pos on screen, y pos on screen))
    def get(self):
        self.bt.update()
        out = [(self.bt.getType(i), (self.bt.getX(i), self.bt.getY(i))) \
            for i in range(self.bt.getNumObj())]
        return out
        
    def __del__(self):
        print "STOPPING"
        self.bt.stop()
        print "STOPPED"
        


class VisionInterfaceDummy:

    def __init__(self):
        pass

    def get(self):
        return [("RED_BALL", (100, 400)), ("GREEN_BALL", (200, 300))]
    
