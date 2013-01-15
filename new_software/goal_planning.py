class GoalPlanning:

    # List of goals
    FIND_BALLS = 0
    SCORE_TOWER = 1
    PRESS_BUTTON = 2
    SCORE_WALL = 3
    WAIT_AT_WALL = 4
    
    START_GOAL = FIND_BALLS
    START_TARGET = None
    
    def __init__(self, state):
        self.state = state
        self.goal = START_GOAL
        self.target = START_TARGET
    
    # Updates current goal according to estimated state
    def run(self):
        pass
        
    # Returns current goal
    def getGoal(self):
        return self.goal
        
    # Returns (distance, angle) if applicable to goal, or None if not applicable
    def getTarget(self):
        return self.target
