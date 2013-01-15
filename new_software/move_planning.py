import time

from Commander import *

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
        self.moveObject = RotateInPlace()
    
    # Gets gaal from GoalPlanning, calculates current move,
    # and calls Control to actuate motors
    def run(self):
        
        if self.move == WALL_FOLLOW:
            pass
            
        elif self.move == MOVE_TO_OPEN:
            pass
            
        elif self.move == ROTATE_IN_PLACE:
            if (self.moveObject == None)
                self.moveObject = new RotateInPlace()
            
        elif self.move == APPROACH_TARGET:
            if (self.moveObject == None)
                self.moveObject = new ApproachTarget()
            
        elif self.move == CAPTURE_BALL:
            pass
            
        elif self.move == ALIGN:
            pass
            
        elif self.move == AVOID_WALL:
            pass

        self.moveObject.run()

class RotateInPlace:
    def __init__(self):
        self.rotateBeginAngle = STATE.getAbsoluteAngle()

    def run(self):
        self.transition()
        self.move()

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

        if goal == GOAL.FIND_BALLS:
            if goal.target != None:
                return MovePlanning.ApproachTarget

    def move(self):
        ctrl(setMovement(0, .5))
        

class ApproachTarget:
    def __init__(self):
        self.targetSpeed = .5
        self.approachBeginTime = time.time()
        self.myPid = Pid(.03, .005, .005, 100)

    def run(self):
        self.transition()
        self.move()

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()
        
        if target == None:
          if goal == GOAL.FIND_BALLS
              return MovePlanning.ROTATE_IN_PLACE

    def move(self):
        (angle, distance) GOAL.getTarget()

        if (not self.myPid.running):
            self.myPid.start(angle, 0)

        pidVal = self.myPid.iterate(angle)
        adjustedSpeed = self.targetSpeed * ((90.0-abs(angle))/90.0)
        ctrl.setMovement(adjustedSpeed, self.rotationSpeed * pidVal)
