import time
import pid
import math

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
    HIT_BUTTON = 5
    ALIGN = 6
    AVOID_WALL = 7
    TIMEOUT_RUN = 8
    SCORE = 9

    def __init__(self):
        self.moveObject = WallFollow()
    
    def run(self):
        self.moveObject = self.moveObject.run()

    def log(self):
        print "~~~MOVE~~~"
        print "Move: " + str(self.moveObject)
        self.moveObject.log()

class Movement():
    def __init__(self):
        self.stopped = False
        self.avoidWalls = True
        self.timeOut = True
        self.startTime = time.time()

        

    def run(self):

        self.myBall = c.STATE().getMyNearestBall()
        self.opBall = c.STATE().getOpNearestBall()
        self.goal = c.STATE().getNearestGoalWall()
        self.button = c.STATE().getNearestButton()

        self.nearestBall = c.STATE().getNearestBall()
        if c.STATE().isButtonUsed():
            self.nearestNonGoalObj = c.STATE().getNearestBallOrGoal()
        else:
            self.nearestNonGoalObj = c.STATE().getNearestNonGoalObj()
        self.nearestObj = c.STATE().getNearestObj()

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
    def log(self):
        pass

class WallFollow(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False)
        self.pid0 = pid.Pid(1, 0, .000, 1)
        self.pid1 = pid.Pid(.01, 0, .000, 1)
        self.d = 0
        self.theta = 0
        self.pidVal0 = 0
        self.pidVal1 = 0
        self.speed = 0
        self.rotation = 0

    def transition(self):
        goal = c.GOAL().getGoal()

        if self.nearestNonGoalObj is not None:
            if goal != c.GOAL().SCORE_AND_LOITER:
                return ApproachTarget()        
        if self.goal is not None:
            if goal != c.GOAL().HUNT:
                return ApproachTarget()

    def move(self):
        pid0 = self.pid0
        pid1 = self.pid1

        (self.d, self.theta) = c.STATE().getWallRelativePos()

        if (not pid0.running):
            pid0.start(self.d, FW_DIST_TARGET)
        if (not pid1.running):
            pid1.start(self.theta, 0)

        self.pidVal0 = pid0.iterate(self.d)
        self.pidVal1 = pid1.iterate(self.theta)
        self.pidVal = self.pidVal0 + self.pidVal1

        self.speed = FW_TRANSLATE_SPEED
        self.rotation = FW_ROTATE_SPEED_SCALE * self.pidVal
        # optional:
        if self.pidVal > 1:
            self.speed /= self.pidVal

        c.CTRL().setMovement(self.speed, self.rotation)

    def log(self):
        print "d = " + str(self.d)
        print "target d = " + str(FW_DIST_TARGET)
        print "theta = " + str(self.theta)
        print "pid0 = " + str(self.pidVal0)
        print "pid1 = " + str(self.pidVal1)
        print "SPD=" + str(self.speed) + ", ROT=" + str(self.rotation)

class MoveToOpen(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.startAngle = c.STATE().getRelativeAngle()
        self.angleMap = []
        self.target = None
        self.pid = pid.Pid(.03, .005, .005, 100)
        self.targetSpeed = .5
        self.speed = 0
        self.rotation = 0

    def transition(self):
        goal = c.GOAL().getGoal()
        distance = c.STATE().getCollisionDistance()

        if distance < .25:
            return WallFollow()

        if self.nearestNonGoalObj is not None:
            if goal != c.GOAL().SCORE_AND_LOITER:
                return approachTarget()        
        if self.goal is not None:
            if goal != c.GOAL().HUNT:
                return approachTarget()

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
            self.speed = adjustedSpeed
            self.rotation = self.rotationSpeed * pidVal
            c.CTRL().setMovement(self.speed, self.rotation)
        else:
            if abs(angle-self.startAngle) < 360: #rotate to find openning
                self.angleMap.append((angle, distance))
                c.CTRL().setMovement(0, .5)
            else: #choose most open angle
                self.target= (0,0)
                for (angle, dist) in self.angleMap:
                    if self.target[1] < dist:
                        self.target = (angle, dist)

    def log(self):
        print "SPD=" + str(self.speed) + ", ROT=" + str(self.rotation)

class CaptureBall(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False)

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.startTime + 2 < time.time():
            c.CTRL().setRoller(False)
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(CPTRBL_TRANSLATE_SPEED, CPTRBL_ROTATE_SPEED)
        c.CTRL().setRoller(True)

class HitButton(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False);

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.startTime + 20 < time.time():
            c.STATE().notifyButtonUsed()
            return WallFollow()   

    def move(self):
        t = time.time() - self.startTime
        if   t > 0 and t < 2   \
          or t > 5 and t < 7   \
          or t > 10 and t < 12 \
          or t > 15 and t < 17:
            c.CTRL().setMovement(HITBTN_TRANSLATE_SPEED, HITBTN_ROTATE_SPEED)
        elif t > 2 and t < 3   \
          or t > 7 and t < 8   \
          or t > 12 and t < 13 \
          or t > 17 and t < 18:
            c.CTRL().setMovement(-1 * HITBTN_TRANSLATE_SPEED, HITBTN_ROTATE_SPEED)
        else:
            c.CTRL().setMovement(0, 0)

class Align(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(1, .000, .000, 100)
        self.d = 0
        self.theta = 0
        self.pidVal = 0
        self.speed = 0
        self.rotation = 0

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.d > 0.4:
            return WallFollow()
        if self.theta < 5 and self.theta > -5:
            return Score()

    def move(self):
        pid = self.pid
        (self.d, self.theta) = c.STATE().getWallRelativePos()
        
        if (not pid.running):
            pid.start(self.theta, 0)

        self.pidVal = pid.iterate(self.theta)
        self.speed = 0
        self.rotation = ALIGN_ROTATE_SPEED_SCALE * self.pidVal
        c.CTRL().setMovement(self.speed, self.rotation)

    def log(self):
        print "d = " + str(self.d)
        print "theta = " + str(self.theta)
        print "pid = " + str(self.pidVal)
        print "SPD=" + str(self.speed) + ", ROT=" + str(self.rotation)

class RotateInPlace(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.startAngle = c.STATE().getRelativeAngle()

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.nearestNonGoalObj is not None:
            if goal != c.GOAL().SCORE_AND_LOITER:
                return approachTarget()        
        if self.goal is not None:
            if goal != c.GOAL().HUNT:
                return approachTarget()

    def move(self):
        c.CTRL().setMovement(ROTINPL_TRANSLATE_SPEED, ROTINPL_ROTATE_SPEED)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.targetSpeed = APPTGT_TRANSLATE_SPEED
        self.rotationSpeed = APPTGT_ROTATE_SPEED
        self.pid = pid.Pid(.03, .005, .005, 100)
        self.target = None
        self.targetType = None
        self.speed = 0
        self.rotation = 0
        self.pidVal = 0

    def transition(self):
        goal = c.GOAL().getGoal()
        
        if goal == c.GOAL().HUNT:
            self.target = self.nearestNonGoalObj
        elif goal == c.GOAL().HUNT_AND_SCORE:
            self.target = self.nearestObj
        elif goal == c.GOAL().SCORE_AND_LOITER:
            self.target = self.goal

        self.targetType = c.STATE().getObjType(self.target)
        t = self.targetType
        if t == None:
            return WallFollow()
        if t == "RED_BALL" or t == "GREEN_BALL":
            if self.target[0] < .22 and abs(self.target[1]) < 12:
                return CaptureBall()
        elif t == "CYAN_BUTTON":
            if c.STATE().getFrontProximity() < 30 and abs(self.target[1]) < 12:
                return HitButton()
        elif t == "YELLOW_WALL":
            if c.STATE().getFrontProximity() < 30:
                return Align()

    def move(self):
        if self.target == None:
            return

        (distance, angle) = self.target

        if (not self.pid.running):
            self.pid.start(angle, 0)

        self.pidVal = self.pid.iterate(angle)

        #slowdown when close, slowdown when off-angle 
        adjustedSpeed = self.targetSpeed if distance > .5 else self.targetSpeed*distance*2
        adjustedSpeed *= ((90.0-abs(angle))/90.0)

        self.speed = adjustedSpeed
        self.rotation = self.rotationSpeed * self.pidVal
        c.CTRL().setMovement(self.speed, self.rotation)

    def pause(self):
        self.pid.stop()

    def log(self):
        print "target type = " + self.targetType
        print "dist from camera = " + str(self.target[0])
        print "dist from sensor = " + str(c.STATE().getFrontProximity())
        print "angle = " + str(self.target[1])
        print "pid = " + str(self.pidVal)
        print "SPD=" + str(self.speed) + ", ROT=" + str(self.rotation)

class Score(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False)

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.startTime + 5 < time.time():
            c.CTRL().setScorer(False)
            c.CTRL().setRamp(0) # what angle exactly?
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(0, 0)
        c.CTRL().setScorer(True)
        c.CTRL().setRamp(90) # what angle exactly?

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
            return WallFollow()

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
                print ""
                nextTime = time.time() + .25
                print timeElapsed
                time.sleep(.02)
            if timeElapsed >= 180:
                c.CTRL().halt()
                break
    except KeyboardInterrupt:
       c.DATA().stopVisionThread()
