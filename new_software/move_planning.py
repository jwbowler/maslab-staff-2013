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
    ALIGN_WITH_WALL = 6
    ALIGN_WITH_TOWER = 7
    ALIGN_WITH_BUTTON = 8
    AVOID_WALL = 9
    TIMEOUT_RUN = 10
    SCORE = 11

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
        self.myBall = None
        self.opBall = None
        self.goalWall = None
        self.tower = None
        self.button = None
        self.nearestBall = None
        self.nearestNonGoalObj = None
        self.nearestObj = None
        

    def run(self):

        self.myBall = c.STATE().getMyNearestBall()
        self.opBall = c.STATE().getOpNearestBall()
        self.goalWall = c.STATE().getNearestGoalWall()
        self.tower = c.STATE().getTowerBase()
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
        self.rotLim = 0.5
        self.pid0 = pid.Pid(1.8, 0, .000, 0.3, 0)
        self.pid1 = pid.Pid(.016, 0, .02, 0.3, 0)
        self.d = 0
        self.theta = 0
        self.pidVal0 = 0
        self.pidVal1 = 0
        self.speed = 0
        self.rotation = 0

    def transition(self):
        
        goal = c.GOAL().getGoal()
        target = None

        if goal == c.GOAL().HUNT:
            target = self.nearestNonGoalObj
        if goal == c.GOAL().HUNT_AND_SCORE:
            target = self.nearestObj
        if goal == c.GOAL().SCORE:
            target = self.tower

        if target is not None:
            return ApproachTarget()
    
    
    def move(self):
        pid0 = self.pid0
        pid1 = self.pid1

        (self.d, self.theta) = c.STATE().getWallPosFrom2Sensors(0, 1)
        #(self.d, self.theta) = c.STATE().getWallRelativePos()

        if (not pid0.running):
            pid0.start(self.d, FW_DIST_TARGET)
        if (not pid1.running):
            pid1.start(self.theta, 0)

        #print (c.STATE().getRawWallDistances()[0], c.STATE().getRawWallDistances()[1])
        #if (c.STATE().getRawWallDistances()[0][0] >= 1000 and c.STATE().getRawWallDistances()[1][0] >= 1000):
            #self.d = 0.5
            #self.theta = 0
        self.pidVal0 = pid0.iterate(self.d)
        self.pidVal1 = pid1.iterate(self.theta)
        self.pidVal = self.pidVal0 + self.pidVal1

        self.speed = FW_SPEED_SCALE
        self.rotation = FW_SPEED_SCALE * self.pidVal
        if self.rotation > self.rotLim:
            self.rotation = self.rotLim
        if self.rotation < -self.rotLim:
            self.rotation = -self.rotLim
        # optional:
        #if self.pidVal > 1:
        #    self.speed /= self.pidVal

        c.CTRL().setMovement(self.speed, self.rotation)
        #c.CTRL().setMovement(0, 0)

    def log(self):
        c.LOG("d = " + str(self.d))
        c.LOG("target d = " + str(FW_DIST_TARGET))
        c.LOG("theta = " + str(self.theta))
        c.LOG("pid0 = " + str(self.pidVal0))
        c.LOG("pid1 = " + str(self.pidVal1))
        c.LOG("SPD=" + str(self.speed) + ", ROT=" + str(self.rotation))

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
            return approachTarget()        
        if self.tower is not None:
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
        c.LOG("SPD=" + str(self.speed) + ", ROT=" + str(self.rotation))

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

class AlignWithWall(Movement):
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
        self.rotation = ALIGN_WALL_ROTATE_SPEED_SCALE * self.pidVal
        c.CTRL().setMovement(self.speed, self.rotation)

    def log(self):
        c.LOG("d = " + str(self.d))
        c.LOG("theta = " + str(self.theta))
        c.LOG("pid = " + str(self.pidVal))
        c.LOG("SPD=" + str(self.speed) + ", ROT=" + str(self.rotation))

class AlignWithTower(Movement):
    def __init__(self):
        Movement.__init__(self)
        self.towerTop = None
        self.pid = pid.Pid(.016, 0, .02, 0.3, 0)
        self.d = 0
        self.baseD = 0
        self.theta = 0
        self.pidVal = 0
        self.speed = 0
        self.rotation = 0

    def transition(self):
        goal = c.GOAL().getGoal()
        if self.baseD > 0.8:
            return ApproachTarget()
        if (-5 < self.theta < 5) and self.d < 0:
            return Score()

    def move(self):
        #self.towerTop = c.STATE().getTowerTop()
        self.towerTop = self.tower
        if self.towerTop is None:
            return
        pid = self.pid
        #self.d = c.STATE().getFrontProximity()
        self.d = self.towerTop[0]
        if self.tower is None:
            self.baseD = 0
        else:
            self.baseD = self.tower[0]
        self.theta = self.towerTop[1]

        if (not pid.running):
            pid.start(self.theta, 0)

        self.pidVal = pid.iterate(-self.theta)
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
        if self.tower is not None:
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
            return

        self.targetType = c.STATE().getObjType(self.target)
        t = self.targetType
        if t == None:
            return WallFollow()
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
        '''    
        # following should never happen given how target is selected
        elif t == "YELLOW_WALL":
            if c.STATE().getFrontProximity() < 30:
                return AlignWithWall()
        '''

    def move(self):
        goal = c.GOAL().getGoal()
        
        if goal == c.GOAL().HUNT:
            self.target = self.nearestNonGoalObj
        elif goal == c.GOAL().HUNT_AND_SCORE:
            self.target = self.nearestObj
        elif goal == c.GOAL().SCORE:
            self.target = self.tower

        if self.target == None:
            return

        (distance, angle) = self.target

        if (not self.pid.running):
            self.pid.start(angle, 0)

        self.pidVal = self.pid.iterate(-angle)

        #slowdown when close, slowdown when off-angle 
        adjustedSpeed = self.targetSpeed if distance > .5 else self.targetSpeed*distance*2
        adjustedSpeed *= ((90.0-abs(angle))/90.0)

        self.speed = adjustedSpeed
        self.rotation = self.rotationSpeed * self.pidVal
        #c.CTRL().setMovement(0, 0)
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
        if self.startTime + 5 < time.time():
            c.CTRL().setScorer(False)
            c.CTRL().setRamp(0) # what angle exactly?
            return WallFollow()   

    def move(self):
        c.CTRL().setMovement(0, 0)
        return
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
                break

    except KeyboardInterrupt:
        pass

    c.CTRL().halt()
    c.DATA().stopVisionThread()
