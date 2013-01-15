import time

from commander import *

class MovePlanning:
    # List of moves
    #wall
    WALL_FOLLOW = 0
    MOVE_TO_OPEN = 1
    ROTATE_IN_PLACE = 2
    APPROACH_TARGET = 3
    CAPTURE_BALL = 4
    ALIGN = 5
    AVOID_WALL = 6
    
    def __init__(self):
        self.moveObject = RotateInPlace()
    
    def run(self):
        self.moveObject = self.moveObject.run()

class Movement():
    stopped = False
    avoidWalls = True

    def run(self):

        if (self.stopped):
            self.stopped = False
            self.resume()

        self.move()
        next = self.transition()
        if next == None: next = self

        if (avoidWalls and STATE.nearCollision()):
            next.stop()
            return AvoidWall(next)

        return next

    def stop(self):
        self.stopped = True
        pause()

    # setters
    def setAvoidWalls(enable):
        self.avoidWalls = enable

    # functions for subclasses to implement
    def move(self):
        pass
    def transition():
        pass
    def pause(self):
        pass
    def resume(self):
        pass 

class WallFollow(Movement):
    def __init__(self):
        pass

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

    def move(self):
        pass

class MoveToOpen(Movement):
    def __init__(self):
        pass

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

    def move(self):
        pass

class CaptureBall(Movement):
    def __init__(self):
        setAvoidWalls(False)
        self.startTime = time.time()

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

        if self.startTime + 2 < time.time():
            CTRL.setRoller(False)
            
            if goal == GOAL.FIND_BALLS:
                if target == None:
                    return RotateInPlace()
                else:
                    return ApproachTarget()
                

    def move(self):
        CTRL.setMove(.5, 0)
        CTRL.setRoller(True)

class Align(Movement):
    def __init__(self):
        pass

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

    def move(self):
        pass

class RotateInPlace(Movement):
    def __init__(self):
        self.startAngle = STATE.getAbsoluteAngle()

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

        if goal == GOAL.FIND_BALLS:
            if goal.target != None:
                return ApproachTarget()

    def move(self):
        CTRL.setMovement(0, .5)

class ApproachTarget(Movement):
    def __init__(self):
        self.targetSpeed = .5
        self.startTime = time.time()
        self.pid = Pid(.03, .005, .005, 100)

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()
        
        if goal == GOAL.FIND_BALLS:
            if target == None:
                return RotateInPlace()
            if target[0] < 15 and target[1] < .18:
                return CaptureBall()

    def move(self):
        (angle, distance) = GOAL.getTarget()

        if (not self.pid.running):
            self.pid.start(angle, 0)

        pidVal = self.pid.iterate(angle)

        #slowdown when close, slowdown when off-angle 
        adjustedSpeed = self.targetSpeed if distance > .33 else self.targetSpeed*distance*3
        adjustedSpeed *= ((90.0-abs(angle))/90.0)

        CTRL.setMovement(adjustedSpeed, self.rotationSpeed * pidVal)

    def pause(self):
        self.pid.stop()

    def resume(self):
        self.startTime = time.time()

class AvoidWall(Movement):
    def __init__(prevMovement):
        self.prevMovement = prevMovement

    def transition(self):
        goal = GOAL.getGoal()
        target = GOAL.getTarget()

        if STATE.nearCollision():
            return self.prevMovement

    def move(self):
        CTRL.setMovement(-.5, 0)
