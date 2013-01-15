import time

import 

class MovePlanning:

    # List of moves
    WALL_FOLLOW = 0
    MOVE_TO_OPEN = 1
    ROTATE_IN_PLACE = 2
    APPROACH_TARGET = 3
    CAPTURE_BALL = 4
    ALIGN = 5
    AVOID_WALL = 6
    
    def __init__(self, state, goal, ctrl):
        self.move = ROTATE_IN_PLACE
        self.moveObject = RotateInPlace()
    
    # Gets gaal from GoalPlanning, calculates current move,
    # and calls Control to actuate motors
    def run(self):
        
        # TODO: Calculate self.move
        
        if self.move == WALL_FOLLOW:
            pass
            
        elif self.move == MOVE_TO_OPEN:
            pass
            
        elif self.move == ROTATE_IN_PLACE:
            rotateInPlace()
            
        elif self.move == APPROACH_TARGET:
            if (self.moveObject == None)
                self.moveObject = new ApproachTarget()
            self.moveObject.run()
            
        elif self.move == CAPTURE_BALL:
            pass
            
        elif self.move == ALIGN:
            pass
            
        elif self.move == AVOID_WALL:
            pass

class RotateInPlace:
    def __init__(self):
        self.rotateBeginAngle = 

class ApproachTarget:
    def __init__(self):
        self.approachBeginTime = time.time()
        self.myPid = Pid(.03, .005, .005, 100)

    def run(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()
        
        if target == None:
          if goal == GOAL.FIND_BALLS
              return MovePlanning.ROTATE_IN_PLACE

        if (not self.myPid.running):
            self.myPid.start(angle, 0)

        angle = -target[1]angle
        pidVal = self.myPid.iterate(angle)
        adjustedSpeed = self.targetSpeed * ((90.0-abs(angle))/90.0)
        ctrl.setMovement(adjustedSpeed, self.rotationSpeed * pidVal)
