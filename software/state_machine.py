

class StateMachine:
    
    def __init__(self, dataCollection, stateDict):
        self.dc = dataCollection
        self.sd = stateDict
        self.currentStateName = self.sd.keys()[0]
        
    def step(self):
        self.data = self.dc.get()
        currentState = self.sd[self.currentStateName]
        print "STATE: " + self.currentStateName
        print "DATA:"
        print self.data
        (output, newStateName) = currentState.step(self.data)
        self.currentStateName = newStateName

    def halt(self):
        self.currentStateName = "HALT"
        self.step(self.data)
        
        
        
class HaltState:
    
    def __init__(self, control):
        self.ctl = control
        
    def step(self):
        ctl.drive(0, 0)
        return (None, None)
