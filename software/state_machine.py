

class StateMachine:
    
    def __init__(dataCollection, stateDict):
        self.dc = dataCollection
        self.sd = stateDict
        self.currentStateName = self.sd.vals[0]
        
    def step():
        currentState = self.sd[self.currentStateName]
        (output, newStateName) = currentState.step()
        self.currentStateName = newStateName

    def halt():
        self.currentStateName = "HALT"
        self.step()
        
        
        
class HaltState:
    
    def __init__(control):
        self.ctl = control
        
    def step()
        ctl.drive(0, 0)
        return (None, None)
