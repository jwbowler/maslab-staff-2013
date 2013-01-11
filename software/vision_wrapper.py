from vision import balltrackingscript

class VisionWrapper:

    def __init__(self, ballTracker):
        self.bt = ballTracker
        self.bt.start()
    
    # Returns list of (sighted object type, (x pos on screen, y pos on screen))
    def get(self):
        self.bt.update()
        return [(self.bt.getType(i), (self.bt.getX(i), self.bt.getY(i))) \
            for i in range(self.bt.getNumObj())]
        
    def __del__(self):
        self.bt.stop()
    
