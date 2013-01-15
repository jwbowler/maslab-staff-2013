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
        self.move = ROTATE_IN_PLACE
    
    # Gets gaal from GoalPlanning, calculates current move,
    # and calls Control to actuate motors
    def run(self):
        
        # TODO: Calculate self.move
        
        if self.move == WALL_FOLLOW:
            pass
            
        elif self.move == MOVE_TO_OPEN:
            pass
            
        elif self.move == ROTATE_IN_PLACE:
            pass
            
        elif self.move == APPROACH_TARGET:
            approachTarget()
            
        elif self.move == CAPTURE_BALL:
            pass
            
        elif self.move == ALIGN:
            pass
            
        elif self.move == AVOID_WALL:
            pass

    def approachTarget(self):
        goal = Goal.getGoal()
        target = Goal.getTarget()
        
        if target == None:
          if goal == Goal.FIND_BALLS
              self.move = ROTATE_IN_PLACE
            
class ApproachTarget:
    def __init__(self, target):
        self.myPid.start(target[1], 0)

    def run(target):
        angle = -target[1]angle
        pidVal = self.myPid.iterate(angle)
        adjustedSpeed = self.targetSpeed * ((90.0-abs(angle))/90.0)
        ctrl.setMovement(adjustedSpeed, self.rotationSpeed * pidVal)
