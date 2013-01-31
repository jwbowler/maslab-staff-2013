import time
import pid
import math

import commander as c
from config import *
import utils

class MovePlanning:
    def __init__(self):
        self.moveObject = WallFollow()
    
    def run(self):
        self.moveObject = self.moveObject.run()

    def log(self):
        c.LOG("~~~MOVE~~~")
        c.LOG("Move: " + str(self.moveObject))

class Movement():
    def __init__(self):
        self.stopped = False
        self.startTime = time.time()

        self.timeOut = time.time() + 100000
        
    def run(self):
        next = self.transition()
        if next == None: next = self
        next.move()
        return next

    def __str__(self):
        return self.__class__.__name__

    # setters
    def setTimeOut(self, time):
        self.timeOut = time

    # functions for subclasses to implement
    def move(self):
        pass
    def transition():
        pass

class TimeoutRun(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setNoTimeout(True)

    def transition(self):
        if time.time() > (self.startTime + 2.0):
            return WallFollow()

    def move(self):
        c.CTRL().setMovement(TMOUT_TRANSLATE_SPEED, TMOUT_ROTATE_SPEED)

class WallFollow(Movement):
    def __init__(self):
        Movement.__init__(self)

        self.distPid = pid.Pid(*WF_DIST_PID)
        self.anglePid = pid.Pid(*WF_ANGLE_PID)

    def transition(self):
        if c.GOAL().getTarget() is not None:
            return ApproachTarget()

    def move(self):
        distPid = self.distPid
        anglePid = self.anglePid

        (dist, angle) = c.STATE().getWallRelativePos(4)
        #(dist, angle) = c.STATE().getWallPosFrom2Sensors(0, 1)
        c.LOG("dist = " + str(dist))
        c.LOG("angle = " + str(angle))

        if (not distPid.running):
            distPid.start(dist, WF_DIST_TARGET)
        if (not anglePid.running):
            anglePid.start(angle, 0)

        distPidVal = distPid.iterate(dist)
        anglePidVal = anglePid.iterate(angle)
        pidVal = distPidVal + anglePidVal
        c.LOG("dist PID = " + str(distPidVal))
        c.LOG("angle PID = " + str(anglePidVal))
        c.LOG("PID = " + str(pidVal))

        speed = WF_SPEED_SCALE
        #blah = c.STATE().getWallDistancesAdjusted()[3][0]
        colDist = c.STATE().getCollisionDistance()
        if colDist < WF_SLOWDOWN_DIST:
            slowRange = WF_SLOWDOWN_DIST-WF_STOP_DIST
            speed *= (slowRange-colDist)/slowRange
        c.LOG("Slowed: " + str(speed))

        

        rotation = WF_ROT_SCALE * pidVal

        c.CTRL().setMovement(speed, rotation)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(*APP_PID)

    def transition(self):
        targetType = c.GOAL().getTargetType()

        if targetType is None:
            return WallFollow()

        (dist, angle) = c.GOAL.getTarget()

        if targetType == c.GOAL().BALL:
            if dist < CPTR_DIST and abs(angle) < CPTR_ANGLE:
                return CaptureBall()
        if targetType == c.GOAL().TOWER:
            if dist < ALIGN_TOWER_DIST and abs(angle) < ALIGN_TOWER_ANGLE:
                return AlignWithTower ()


    def move(self):
        (dist, angle) = c.GOAL.getTarget()

        if (not self.pid.running):
            self.pid.start(-angle, 0)

        self.pidVal = self.pid.iterate(-angle)

        speed = APP_TRANSLATE_SPEED * ((90.0-abs(angle))/90.0)
        if dist < APP_SLOWDOWN_DIST:
            speed *= (APP_SLOWDOWN_DIST-dist)/APP_SLOWDOWN_DIST

        rotation = APR_ROTATION * self.pidVal

        c.CTRL().setMovement(speed, rotation)

class CaptureBall(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        if self.startTime + CPTR_TIME < time.time():
            c.CTRL().setRoller(False)
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(CPTR_SPEED, 0)
        c.CTRL().setRoller(True)
        c.CTRL().setHelix(True)

class HitButton(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        if self.startTime + HIT_TIME < time.time():
            c.CTRL().setRoller(False)
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(HIT_SPEED, 0)

class AlignWithTower(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(*ALIGN_TOWER_PID)

    def transition(self):
        midTower = c.STATE().getTowerMiddle()

        if midTower is None:
            return WallFollow()

        (dist, angle) = midTower

        if dist < SCORE_DIST and abs(angle) < SCORE_ANGLE:
            return Score()

    def move(self):
        mitTower = c.STATE().getTowerMiddle()

        if midTower is None:
            return

        pid = self.pid
        self.d = c.STATE().getTowerMiddle()[0]
        self.theta = -c.STATE().getTowerMiddle()[1]

        if (not pid.running):
            pid.start(self.theta, 0)

        self.pidVal = pid.iterate(self.theta)
        self.speed = ALIGN_TOWER_TRANSLATE_SPEED
        self.rotation = ALIGN_TOWER_ROTATE_SPEED_SCALE * self.pidVal
        c.CTRL().setMovement(self.speed, self.rotation)

class AlignWithButton(Movement):
    def __init__(self):
        pass

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.d > 0.4:
            return WallFollow()
        if self.theta < 5 and self.theta > -5:
            return Score()

    def move(self):
        pass

class RotateInPlace(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.nearestNonGoalObj is not None:
            return approachTarget()        
        if c.STATE().getTowerMiddle() is not None:
            if goal != c.GOAL().HUNT:
                return approachTarget()

    def move(self):
        c.CTRL().setMovement(ROTINPL_TRANSLATE_SPEED, ROTINPL_ROTATE_SPEED)

class Score(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        goal = c.GOAL().getGoal()
        if time.time() > self.startTime + 5:
            c.CTRL().setRamp(0) # what angle exactly?
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(0, 0)
        return
        c.CTRL().setRamp(90) # what angle exactly?
