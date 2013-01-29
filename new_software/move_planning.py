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
        self.moveObject.log()

class Movement():
    def __init__(self):
        self.stopped = False
        self.avoidWalls = True
        self.timeOut = True
        self.startTime = time.time()
        self.nearestNonGoalObj = None
        
    def run(self):

        if c.STATE().isButtonUsed():
            self.nearestNonGoalObj = c.STATE().getNearestBallOrGoal()
        else:
            self.nearestNonGoalObj = c.STATE().getNearestNonGoalObj()

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

        self.rotLim = 0.5
        self.distPid = pid.Pid(2.8, 0, .000, 0.3, 0)
        self.anglePid = pid.Pid(.08, 0, .02, 0.4, 0)

    def transition(self):
        '''
        goal = c.GOAL().getGoal()
        target = None

        if goal == c.GOAL().HUNT:
            target = c.STATE().getNearestNonGoalObj()
        if goal == c.GOAL().HUNT_AND_SCORE:
            target = c.STATE().getNearestObj()
        if goal == c.GOAL().SCORE:
            target = c.STATE().getTowerMiddle()

        if target is not None:
            return ApproachTarget()
        '''

    def move(self):
        distPid = self.distPid
        anglePid = self.anglePid

        #(dist, theta) = c.STATE().getWallPosFrom2Sensors(0, 1)
        (dist, theta) = c.STATE().getWallRelativePos(4)

        if (not distPid.running):
            distPid.start(dist, FW_DIST_TARGET)
        if (not anglePid.running):
            anglePid.start(theta, 0)

        pidVal = distPid.iterate(dist) + anglePid.iterate(theta)

        speed = FW_SPEED_SCALE
        rotation = FW_SPEED_SCALE * pidVal

        c.CTRL().setMovement(speed, utils.absBound(rotation, self.rotLim))

        if MOVE_LOG:
            c.LOG("d = " + str(dist))
            c.LOG("target d = " + str(FW_DIST_TARGET))
            c.LOG("theta = " + str(theta))
            c.LOG("distPid = " + str(self.distPid.getLastOutput()))
            c.LOG("anglePid = " + str(self.anglePid.getLastOutput()))
            c.LOG("SPD=" + str(speed) + ", ROT=" + str(rotation))

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
        #self.d = c.STATE().getFrontProximity()
        self.d = c.STATE().getTowerMiddle()[0]
        self.theta = -c.STATE().getTowerMiddle()[1]

        if (not pid.running):
            pid.start(self.theta, 0)

        self.pidVal = pid.iterate(self.theta)
        self.speed = ALIGN_TOWER_TRANSLATE_SPEED
        self.rotation = ALIGN_TOWER_ROTATE_SPEED_SCALE * self.pidVal
        #c.CTRL().setMovement(0, 0)
        c.CTRL().setMovement(self.speed, self.rotation)

    def log(self):
        c.LOG("d = " + str(self.d))
        c.LOG("theta = " + str(self.theta))
        c.LOG("pid = " + str(self.pidVal))
        c.LOG("SPD=" + str(self.speed) + ", ROT=" + str(self.rotation))

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

    def log(self):
        pass

class RotateInPlace(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.startAngle = c.STATE().getRelativeAngle()

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.nearestNonGoalObj is not None:
            return approachTarget()        
        if c.STATE().getTowerMiddle() is not None:
            if goal != c.GOAL().HUNT:
                return approachTarget()

    def move(self):
        c.CTRL().setMovement(ROTINPL_TRANSLATE_SPEED, ROTINPL_ROTATE_SPEED)

class ApproachTarget(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.targetSpeed = APPTGT_TRANSLATE_SPEED
        self.rotationSpeed = APPTGT_ROTATE_SPEED
        self.pid = pid.Pid(.03, .000, .000, .2, 100)
        self.target = None
        self.targetType = None
        self.speed = 0
        self.rotation = 0
        self.pidVal = 0
        

    def transition(self):
        if self.target is None:
            return WallFollow()

        self.targetType = c.STATE().getObjType(self.target)
        t = self.targetType

        if t == "RED_BALL" or t == "GREEN_BALL":
            if self.target[0] < .22 and abs(self.target[1]) < 12:
                return CaptureBall()
        elif t == "CYAN_BUTTON":
            if c.STATE().getFrontProximity() < 30 and abs(self.target[1]) < 12:
                return AlignWithButton()
        #elif t == "PURPLE_GOAL":
        elif t == "YELLOW_WALL":
            d = self.target[0]
            if d < .7:
                return AlignWithTower()

    def move(self):
        goal = c.GOAL().getGoal()
        
        if goal == c.GOAL().HUNT:
            self.target = self.nearestNonGoalObj
        elif goal == c.GOAL().HUNT_AND_SCORE:
            self.target = c.STATE().getNearestObj()
        elif goal == c.GOAL().SCORE:
            self.target = c.STATE().getTowerMiddle()

        if self.target == None:
            return

        (distance, angle) = self.target
        angle = -angle

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
        if self.target is None:
            c.LOG("no target")
            return
        c.LOG("target type = " + self.targetType)
        c.LOG("dist from camera = " + str(self.target[0]))
        c.LOG("dist from sensor = " + str(c.STATE().getFrontProximity()))
        c.LOG("angle = " + str(self.target[1]))
        c.LOG("pid = " + str(self.pidVal))
        c.LOG("SPD=" + str(self.speed) + ", ROT=" + str(self.rotation))

class Score(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.setAvoidWalls(False)

    def transition(self):
        goal = c.GOAL().getGoal()
        if time.time() > self.startTime + 5:
            c.CTRL().setRamp(0) # what angle exactly?
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(0, 0)
        return
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
