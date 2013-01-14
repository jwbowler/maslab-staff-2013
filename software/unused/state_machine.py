log = True

class StateMachine:
    
    def __init__(self, dataCollection, stateDict):
        self.dc = dataCollection
        self.sd = stateDict
        self.currentStateName = self.sd.keys()[0]
        
    def step(self):
        self.data = self.dc.get()
        currentState = self.sd[self.currentStateName]
        if log:
            print "STATE: " + self.currentStateName
        (output, newStateName) = currentState.step(self.data)
        self.currentStateName = newStateName

    def halt(self):
        self.currentStateName = "HALT"
        currentState = self.sd[self.currentStateName]
        currentState.step()
        
        
        
class HaltState:
    
    def __init__(self, control):
        self.ctl = control
        
    def step(self):
        self.ctl.drive(0, 0)
        return (None, None)
