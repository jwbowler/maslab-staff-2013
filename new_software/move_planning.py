import time
import pid

import commander as c
from config import *

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
        self.moveObject = WallFollow()
    
    def run(self):
        self.moveObject = self.moveObject.run()

    def log(self):
        #print "~~~MOVE~~~"
        print self.moveObject
        #print "~~~MOVE~~~"

class Movement():
    def __init__(self):
        self.stopped = False
        self.avoidWalls = True
        self.timeOut = True
        self.startTime = time.time()

    def run(self):

        if (self.stopped):
            self.stopped = False
            self.startTime = time.time()
            self.resume()

        self.move()
        next = self.transition()
        if next == None: next = self

        if (self.avoidWalls and c.STATE().nearCollision()):
            next.stop()
            return AvoidWall(next)

        return next

    def stop(self):
        self.stopped = True
        self.pause()

    def __str__(self):
        return self.__class__.__name__

    # setters
    def setAvoidWalls(self, enable):
        self.avoidWalls = enable

    def setTimeOut(self, enable):
        self.timeOut = enable

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
        Movement.__init__(self)
        self.setAvoidWalls(False)
        self.goalDist = .45
        self.linear = .2
        self.rotation = .2
        # -85 40 0
        self.pidArray = []
        self.pidArray.append(pid.Pid(1.0, .000, .000, 100))
        self.pidArray.append(pid.Pid(.0, .000, .000, 100))
        self.pidArray.append(pid.Pid(.0, .000, .000, 100))

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()

        if goal == c.GOAL().FIND_BALLS:
            if target != None:
                return ApproachTarget()

    def move(self):
        wallDistances = c.STATE().getWallDistances()
        pidVals = []
        for i in xrange(len(self.pidArray)):
            pid = self.pidArray[i]
            (angle, distance) = wallDistances[i]
            goal = self.goalDist * math.sin(math.radians(abs(angle)))
            if (not pid.running):
                pid.start(distance, goal)

            pidVals.append(self.pid.iterate(angle))

        #slowdown when close, slowdown when off-angle 
        collision = c.STATE().getCollisionDistance()
        #adjustedSpeed = self.targetSpeed if collision > .5 else self.targetSpeed*collision*2

        c.CTRL().setMovement(adjustedSpeed, self.rotationSpeed * sum(pidVals))

class MoveToOpen(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.startAngle = c.STATE().getRelativeAngle()
        self.angleMap = []
        self.target = None

        self.pid = pid.Pid(.03, .005, .005, 100)
        self.targetSpeed = .5

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()
        distance = c.STATE().getCollisionDistance()

        if goal == c.GOAL().FIND_BALLS:
            if target != None:
                return ApproachTarget()
            else:
                if distance < .25:
                    return WallFollow()

    def move(self):
        angle = c.STATE().getRelativeAngle()
        distance = c.STATE().getCollisionDistance()

        if self.target != None: #go in most open direction
            if (not self.pid.running):
                self.pid.start(angle, self.target[0])

            pidVal = self.pid.iterate(angle)

            #slowdown when close, slowdown when off-angle 
            adjustedSpeed = self.targetSpeed if distance > .33 else self.targetSpeed*distance*3
            adjustedSpeed = 0 if angle > 15 else ((30.0-abs(angle))/30.0)

            c.CTRL().setMovement(adjustedSpeed, self.rotationSpeed * pidVal)
        else:
            if abs(angle-self.startAngle) < 360: #rotate to find openning
                self.angleMap.append((angle, distance))
                c.CTRL().setMovement(0, .5)
            else: #choose most open angle
                self.target= (0,0)
                for (angle, dist) in self.angleMap:
                    if self.target[1] < dist:
                        self.target = (angle, dist)

class CaptureBall(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False)

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()

        if self.startTime + 2 < time.time():
            c.CTRL().setRoller(False)
            
            if goal == c.GOAL().FIND_BALLS:
                if target == None:
                    return RotateInPlace()
                else:
                    return ApproachTarget()
                

    def move(self):
        c.CTRL().setMovement(CPTRBL_TRANSLATE_SPEED, CPTRBL_ROTATE_SPEED)
        c.CTRL().setRoller(True)

class Align(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()

    def move(self):
        pass

class RotateInPlace(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.startAngle = c.STATE().getRelativeAngle()

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()

        if goal == c.GOAL().FIND_BALLS:
            if target != None:
                return ApproachTarget()

    def move(self):
        c.CTRL().setMovement(ROTINPL_TRANSLATE_SPEED, ROTINPL_ROTATE_SPEED)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.targetSpeed = APPTGT_TRANSLATE_SPEED
        self.rotationSpeed = APPTGT_ROTATE_SPEED
        self.pid = pid.Pid(.03, .005, .005, 100)

    def transition(self):
        goal = c.GOAL().getGoal()
        target = c.GOAL().getTarget()
        
        if goal == c.GOAL().FIND_BALLS:
            if target == None:
                return RotateInPlace()
            if target[0] < .22 and abs(target[1]) < 12:
                return CaptureBall()

    def move(self):
        target = c.GOAL().getTarget()
        if target == None:
            return

        (distance, angle) = target

        if (not self.pid.running):
            self.pid.start(angle, 0)

        pidVal = self.pid.iterate(angle)

        #slowdown when close, slowdown when off-angle 
        adjustedSpeed = self.targetSpeed if distance > .5 else self.targetSpeed*distance*2
        adjustedSpeed *= ((90.0-abs(angle))/90.0)

        c.CTRL().setMovement(adjustedSpeed, self.rotationSpeed * pidVal)

    def pause(self):
        self.pid.stop()


class AvoidWall(Movement):
    def __init__(self, prevMovement):
        Movement.__init__(self)
        self.setAvoidWalls(False)
        self.prevMovement = prevMovement

    def transition(self):
        if time.time() > (self.startTime + 1.0) and not c.STATE().nearCollision():
            return self.prevMovement

    def move(self):
        c.CTRL().setMovement(AVDWLL_TRANSLATE_SPEED, AVDWLL_ROTATE_SPEED)

class TimeoutRun(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setNoTimeout(True)
        self.hitWall = False

    def transition(self):
        if self.hitWall:
            return RotateInPlace()

    def move(self):
        c.CTRL().setMovement(TMOUT_TRANSLATE_SPEED, TMOUT_ROTATE_SPEED)

    def resume(self):
        self.hitWall = True

if __name__ == "__main__":
    c.ARD()
    c.DATA()
    c.STATE()
    c.GOAL()
    c.MOVE()
    c.CTRL()
    c.ARD().run()

    nextTime = time.time() + .5

    startTime = time.time()

    try:
        while True:
            c.DATA().run()

            c.STATE().run()

            c.GOAL().run()

            c.MOVE().run()

            timeElapsed = time.time() - startTime 
            if time.time() > nextTime:
                c.STATE().log()
                c.GOAL().log()
                c.MOVE().log()
                nextTime = time.time() + .5
                print timeElapsed
            if timeElapsed >= 180:
                c.CTRL().halt()
                break
    except KeyboardInterrupt:
       c.DATA().stopVisionThread()
