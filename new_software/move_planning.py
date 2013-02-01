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
        if time.time() > self.timeOut:
            next = TimeoutRun()
        next.move()
        return next

    def __str__(self):
        return self.__class__.__name__

    # setters
    def setTimeOut(self, time):
        self.timeOut = time + self.startTime

    # functions for subclasses to implement
    def move(self):
        pass
    def transition():
        pass

class TimeoutRun(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        if time.time() > (self.startTime + 1):
            return WallFollow()

    def move(self):
        c.CTRL().setMovement(TMOUT_TRANSLATE_SPEED, TMOUT_ROTATE_SPEED)

class WallFollow(Movement):
    def __init__(self):
        Movement.__init__(self)

        self.distPid = pid.Pid(*WF_DIST_PID)
        self.anglePid = pid.Pid(*WF_ANGLE_PID)

        self.setTimeOut(WF_TIMEOUT)

    def transition(self):
        if c.GOAL().getTarget() is not None:
            return ApproachTarget()

        pass

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

        speed = WF_SPEED
        (colDist, colAngle) = c.STATE().getCollisionDistance()
        if colDist < WF_SLOWDOWN_DIST:
            slowRange = WF_SLOWDOWN_DIST-WF_STOP_DIST
            speed *= (colDist-WF_STOP_DIST)/slowRange


        c.LOG("Slowed: " + str(speed))

        rotation = WF_ROTATION * pidVal

        maxWheel = abs(speed) + abs(rotation)
        if maxWheel < WF_MIN_WHEEL_SPEED:
            rotation = math.copysign(WF_MIN_WHEEL_SPEED-abs(speed), rotation)

        c.CTRL().setMovement(speed, rotation)
        c.CTRL().setRamp(NORMAL_RAMP_ANGLE)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(*APP_PID)
        self.setTimeOut(APP_TIMEOUT)

    def transition(self):
        targetType = c.GOAL().getTargetType()

        if targetType is None:
            return WallFollow()

        (dist, angle) = c.GOAL().getTarget()

        if targetType == c.GOAL().BALL:
            if dist < CPTR_DIST and abs(angle) < CPTR_ANGLE:
                return CaptureBall()
        if targetType == c.GOAL().TOWER:
            c.LOG("TARGET = TOWER")
            c.LOG(dist)
            c.LOG(ALIGN_TOWER_DIST)
            c.LOG(angle)
            c.LOG(ALIGN_TOWER_ANGLE)
            if dist < ALIGN_TOWER_DIST and abs(angle) < ALIGN_TOWER_ANGLE:
                return AlignWithTower ()


    def move(self):
        (dist, angle) = c.GOAL().getTarget()

        if (not self.pid.running):
            self.pid.start(-angle, 0)

        self.pidVal = self.pid.iterate(-angle)

        speed = APP_SPEED * ((90.0-abs(angle))/90.0)
        if dist < APP_SLOWDOWN_DIST:
            speed *= dist/APP_SLOWDOWN_DIST

        rotation = APP_ROTATION * self.pidVal

        (colDist, colAngle) = c.STATE().getCollisionDistance()
        if colDist < APP_WALL_SLOWDOWN_DIST:
            slowRange = APP_WALL_SLOWDOWN_DIST-APP_WALL_STOP_DIST
            speed *= (colDist-APP_WALL_STOP_DIST)/slowRange
            rotation = -math.copysign(APP_K_WALL_AVOID*(APP_WALL_SLOWDOWN_DIST - colDist), colAngle)

        maxWheel = abs(speed) + abs(rotation)
        if maxWheel < APP_MIN_WHEEL_SPEED:
            rotation = math.copysign(APP_MIN_WHEEL_SPEED-abs(speed), rotation)


        c.LOG("Slowed: " + str(speed))

        c.CTRL().setMovement(speed, rotation)

class CaptureBall(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        if self.startTime + CPTR_TIME * (5.0/4) < time.time():
            return WallFollow()   

    def move(self):
        if time.time() - self.startTime < (CPTR_TIME*(2.0/4)):
            c.CTRL().setMovement(CPTR_SPEED, 0)
        elif time.time() - self.startTime < (CPTR_TIME*(3.0/4)):
            c.CTRL().setMovement(CPTR_SPEED/2.0, -CPTR_SPEED/2.0)
        elif time.time() - self.startTime < (CPTR_TIME*(4.0/4)):
            c.CTRL().setMovement(CPTR_SPEED/2.0, CPTR_SPEED/2.0)
        else:
            c.CTRL().setMovement(-CPTR_SPEED, 0)

class HitButton(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        if self.startTime + HIT_TIME < time.time():
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(HIT_SPEED, 0)

class AlignWithTower(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(*ALIGN_TOWER_PID)

    def transition(self):
        tower = c.STATE().getTowerTop()

        if tower is None:
            return WallFollow()

        (dist, angle) = tower

        #if dist < SCORE_DIST and abs(angle) < SCORE_ANGLE:
        if time.time() - self.startTime > 6:
            return Score()

    def move(self):
        tower = c.STATE().getTowerTop()

        if tower is None:
            return

        pid = self.pid
        self.d = c.STATE().getTowerTop()[0]
        c.LOG("dist = " + str(self.d))
        self.theta = -c.STATE().getTowerTop()[1]
        c.LOG("angle = " + str(self.theta))

        if (not pid.running):
            pid.start(self.theta, 0)

        self.pidVal = pid.iterate(self.theta)
        c.LOG("pidVal = " + str(self.pidVal))
        if time.time() - self.startTime < 3:
            self.speed = ALIGN_TOWER_TRANSLATE_SPEED
        else:
            self.speed = 0
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
        if time.time() - self.startTime >= 9:
            c.CTRL().setRamp(NORMAL_RAMP_ANGLE)
            c.STATE().notifyScore()
            return WallFollow()   

    def move(self):
        if time.time() - self.startTime < 4:
            c.CTRL().setMovement(0, 0)
            c.CTRL().setRamp(BLUE_GOAL_RAMP_ANGLE)
        elif 4 <= time.time() - self.startTime < 6:
            c.CTRL().setMovement(-.15, .1)
        else:
            c.CTRL().setMovement(-.15, 0)

