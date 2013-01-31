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

        self.timeOut = time.time() + 10000
        
    def run(self):
        self.move()
        next = self.transition()
        if next == None: next = self

        if (time.time() > self.timeOut):
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

        self.distPid = pid.Pid(2.8, 0, .000, 0.3, 0)
        self.anglePid = pid.Pid(.08, 0, .02, 0.4, 0)

    def transition(self):
        if c.GOAL().getTarget() is not None:
            return ApproachTarget()

    def move(self):
        distPid = self.distPid
        anglePid = self.anglePid

        (dist, theta) = c.STATE().getWallRelativePos(4)

        if (not distPid.running):
            distPid.start(dist, FW_DIST_TARGET)
        if (not anglePid.running):
            anglePid.start(theta, 0)

        pidVal = distPid.iterate(dist) + anglePid.iterate(theta)

        speed = FW_SPEED_SCALE
        rotation = FW_ROT_SCALE * pidVal

        c.CTRL().setMovement(speed, rotation)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)

        self.pid = pid.Pid(.03, .000, .000, .2, 100)

    def transition(self):
        if self.target is None:
            return WallFollow()

        if goal == c.GOAL().HUNT:
            if self.target[0] < CPTR_DIST and abs(self.target[1]) < CPTR_ANGLE:
                return CaptureBall()
        if goal == c.GOAL().BUTTON:

            self.target = c.STATE().getButton()
        if goal == c.GOAL().SCORE:
            self.target = c.STATE().getTowerMiddle()

    def move(self):
        if goal == c.GOAL().HUNT:
            self.target = c.STATE().getNearestBall()
        if goal == c.GOAL().BUTTON:
            self.target = c.STATE().getButton()
        if goal == c.GOAL().SCORE:
            self.target = c.STATE().getTowerMiddle()

        if self.target == None:
            return

        (distance, angle) = self.target

        if (not self.pid.running):
            self.pid.start(-angle, 0)

        self.pidVal = self.pid.iterate(-angle)

        #slowdown when close, slowdown when off-angle 
        adjustedSpeed = self.targetSpeed if distance > .5 else self.targetSpeed*distance*2
        adjustedSpeed *= ((90.0-abs(angle))/90.0)

        speed = adjustedSpeed
        rotation = APR_ROTATION * self.pidVal
        c.CTRL().setMovement(speed, rotation)

    def pause(self):
        self.pid.stop()

class CaptureBall(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.startTime + 2 < time.time():
            c.CTRL().setRoller(False)
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(CPTRBL_TRANSLATE_SPEED, CPTRBL_ROTATE_SPEED)
        c.CTRL().setRoller(True)
        c.CTRL().setRoller(True)
        c.CTRL().setHelix(True)

class HitButton(Movement):
    def __init__(self):
        Movement.__init__(self)

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.startTime + 20 < time.time():
            c.STATE().notifyButtonUsed()
            return WallFollow()   

    def move(self):
        # Cycle through the following steps 4 times:
        # - Drive forward for 2 seconds
        # - Wait for 8 seconds
        # - Drive backward for 1 second
        # - Wait for BALL_BUTTON_TIMEOUT - 2 - 8 - 1 = 11 seconds
        t = time.time() - self.startTime
        for i in range(4):
            a = BALL_BUTTON_TIMEOUT * i
            if t >= a and t < a + 2:
                c.CTRL().setMovement(HITBTN_TRANSLATE_SPEED, HITBTN_ROTATE_SPEED)
                break
            elif t >= a + 10 and t < a + 11:
                c.CTRL().setMovement(-1 * HITBTN_TRANSLATE_SPEED, HITBTN_ROTATE_SPEED)
                break
            else:
                c.CTRL().setMovement(0, 0)

class AlignWithTower(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.pid = pid.Pid(.016, 0, .02, 0.3, 0)
        self.d = 0
        self.theta = 0
        self.pidVal = 0
        self.speed = 0
        self.rotation = 0

    def transition(self):
        midTower = c.STATE().getTowerMiddle()

        if midTower is None:
            return WallFollow()
        if midTower[0] > 0.8:
            return ApproachTarget()
        if (-5 < self.theta < 5) and self.d < .45:
            return Score()

    def move(self):
        if c.STATE().getTowerMiddle() is None:
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
