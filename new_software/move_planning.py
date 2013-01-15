class MovePlanning:

    # List of moves
    WALL_FOLLOW = 0
    MOVE_TO_OPEN = 1
    ROTATE_IN_PLACE = 2
    APPROACH_TARGET = 3
    CAPTURE_BALL = 4
    ALIGN = 5
    AVOID_WALL = 6
    
    def __init__(self):
    
    # Gets gaal from GoalPlanning, calculates current move,
    # and calls Control to actuate motors
    def run(self):
        
        goal = Goal.getGoal()
        target = Goal.getTarget()
        
        # TODO: Calculate self.move
        
        if self.move == WALL_FOLLOW:
            pass
            
        if self.move == MOVE_TO_OPEN:
            pass
            
        if self.move == ROTATE_IN_PLACE:
            pass
            
        if self.move == APPROACH_TARGET:
            pass
            
        if self.move == CAPTURE_BALL:
            pass
            
        if self.move == ALIGN:
            pass
            
        if self.move == AVOID_WALL:
            pass
            
        
    
