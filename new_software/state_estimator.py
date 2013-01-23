import commander as c
import time
import math
from config import *

class StateEstimator:

    # takes data object
    def __init__(self):
        self.data = c.DATA()
        self.startTime = time.time()
        self.timeLastScore = 0
        self.buttonUsed = False
        self.relativeAngle = None
        self.lastImageStamp = None
        self.myBalls = []
        self.opBalls = []
        self.goalWalls = []
        self.buttons = []
        self.wallDistRaw = []
        self.wallDistTimeoutFixed = []
        self.wallDistLowpass = []
        self.wallDistOutliersFixed = []
        self.wallDistCorrected = []
    
    # Updates estimated state according to data in Data class
    def run(self):
        #self.computeRelativeAngle()

        cam = self.data.getCamera()
        if cam.hasNewFrame():
            self.myBalls = sorted(cam.getMyReachableBalls(), key=lambda obj: obj[0])
            self.opBalls = sorted(cam.getOpReachableBalls(), key=lambda obj: obj[0])
            self.goalWalls = sorted(cam.getReachableGoalWalls(), key=lambda obj: obj[0])
            self.buttons = sorted(cam.getReachableButtons(), key=lambda obj: obj[0])
            self.angleAtLastFrame = self.relativeAngle
        elif False:
            shift = self.relativeAngle - self.angleAtLastFrame
            self.myBalls = [(b[0], b[1]+shift) for b in self.myBalls]
            self.opBalls = [(b[0], b[1]+shift) for b in self.opBalls]
            self.goalWalls = [(w[0], w[1]+shift) for w in self.goalWalls]
            self.buttons = [(b[0], b[1]+shift) for b in self.buttons]

        # set wallDistRaw
        dist = [ir.getPosition() for ir in self.data.getIr()]
        dist.extend([ult.getPosition() for ult in self.data.getUlt()])
        self.wallDistRaw = dist[:]

        # set wallDistTimeoutFixed
        if self.wallDistCorrected != []:
            for i in xrange(len(dist)):
                if dist[i][0] > 1000:
                    dist[i] = self.wallDistCorrected[i]
        self.wallDistTimeoutFixed = dist[:]

        # set wallDistLowpass
        blurAmount = .8
        if self.wallDistLowpass != []:
            for i in xrange(len(dist)):
                corrDist = self.wallDistLowpass[i][0] * blurAmount + dist[i][0] * (1 - blurAmount)
                self.wallDistLowpass[i] = (corrDist, self.wallDistLowpass[1])
        else:
            self.wallDistLowpass = dist[:]
        
        # set wallDistOutliersFixed
        errorCutoff = .25
        if self.wallDistOutliersFixed != []:
            for i in xrange(len(dist)):
                if dist[i][0] > (1 + errorCutoff) * self.wallDistLowpass[i][0] \
                 or dist[i][0] < (1 - errorCutoff) * self.wallDistLowpass[i][0]:
                    dist[i] = self.wallDistLowpass[i]
        self.wallDistOutliersFixed = dist[:]

        # set wallDistCorrected
        self.wallDistCorrected = self.wallDistTimeoutFixed[:]

    def log(self):
        print "~~~State Log~~~"

        print "My Balls"
        print self.getMyBalls()

        print "Opponent Balls"
        print self.getOpBalls()

        print "Buttons"
        print self.getButtons()

        print "Goal Walls"
        print self.getGoalWalls()

        print "Raw Wall Distances"
        print self.getRawWallDistances()

        print "Corrected Wall Dist"
        print self.getWallDistances()

        print "Collision Distance"
        print self.getCollisionDistance()

        print "Near Collision?"
        print self.nearCollision()


    def getTimeRemaining(self):
        if TIME_BEFORE_HALT <= 0:
            return 999
        return self.startTime + TIME_BEFORE_HALT - time.time()

    def notifyButtonUsed(self):
        self.buttonUsed = True

    def isButtonUsed(self):
        return self.buttonUsed

    def notifyScore(self):
        self.timeLastScore = time.time()

    def getTimeSinceLastScore(self):
        return time.time() - self.timeLastScore

    def computeRelativeAngle():
        compass = c.DATA().getImu().getCompassHeading()
        if self.relativeAngle == None:
            self.relativeAngle = compass
        else:
            delta = compass = self.relativeAngle
            if delta > 180:
                delta -= 360
            elif delta < 180:
                delta += 360

            #shift, then ensure that angle is in sync with imu
            self.relativeAngle += delta
            #not sure if necessary...
            self.relativeAngle = math.round((self.relativeAngle-compass)/360.0)*360 + compass
        
        
    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getMyBalls(self):
        return self.myBalls
        
    # Returns (distance, angle) of nearest ball
    def getMyNearestBall(self):
        if len(self.myBalls) == 0:
            return None
        return self.myBalls[0]

    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getOpBalls(self):
        return self.opBalls
        
    # Returns (distance, angle) of nearest ball
    def getOpNearestBall(self):
        if len(self.opBalls) == 0:
            return None
        return self.opBalls[0]

    def getGoalWalls(self):
        return self.goalWalls
        
    def getNearestGoalWall(self):
        if len(self.goalWalls) == 0:
            return None
        return self.goalWalls[0]

    def getButtons(self):
        return self.buttons
        
    def getNearestButton(self):
        if len(self.buttons) == 0:
            return None
        return self.buttons[0]

    def getObjType(self, obj):
        if obj in self.myBalls:
            if MY_BALLS_ARE_RED:
                return "RED_BALL"
            else:
                return "GREEN_BALL"
        if obj in self.opBalls:
            if MY_BALLS_ARE_RED:
                return "GREEN_BALL"
            else:
                return "RED_BALL"
        if obj in self.goalWalls:
            return "YELLOW_WALL"
        if obj in self.buttons:
            return "CYAN_BUTTON"
        else:
            return None

    def getNearestBall(self):
        m = self.getMyNearestBall()
        o = self.getOpNearestBall()
        if m == None and o == None:
            return None
        elif m == None or m[0] > o[0]:
            return o
        else:
            return m

    def getNearestBallOrGoal(self):
        ball = self.getNearestBall()
        goal = self.getNearestGoalWall()
        if ball == None and goal == None:
            return None
        elif ball == None or ball[0] > goal[0]:
            return goal
        else:
            return ball

    def getNearestNonGoalObj(self):
        ball = self.getNearestBall()
        button = self.getNearestButton()
        if ball == None and button == None:
            return None
        elif ball == None or ball[0] > button[0]:
            return button
        else:
            return ball

    def getNearestObj(self):
        nonGoal = self.getNearestNonGoalObj()
        goal = self.getNearestGoalWall()
        if nonGoal == None and goal == None:
            return None
        elif nonGoal == None or nonGoal[0] > goal[0]:
            return goal
        else:
            return nonGoal
      
    # Returns fully corrected set of wall distances ond angles from all sensors:
    # ((distance, angle), (distance, angle), ...)
    def getWallDistances(self):
        return self.wallDistCorrected

    # Returns wall distances without any corrections
    def getRawWallDistances(self):
        return self.wallDistRaw

    # Returns the forward distance that the robot can travel
    # before it hits a wall
    def getCollisionDistance(self):
        dist = self.getWallDistances()
        dist = [p[0]/math.cos(math.radians(p[1])) - ROBOT_RADIUS for p in dist]
        dist = [d for d in dist if d > 0]
        return min(dist)


    def nearCollision(self):
        return (self.getCollisionDistance() < .12)
    
    # Takes two sensor indices to use for wall estimation
    # Returns (distance to wall, angle of wall relative to bot's orientation)
    def getPosRelativeToWall(self, index0, index1):
        sensorList = self.getWallDistances()
        sensorA = sensorList[index0]
        sensorB = sensorList[index1]
        phi = .5 * abs(sensorA[1] - sensorB[1])
        a = sensorA[0]
        b = sensorB[0]
        theta = math.asin(math.sqrt((abs(a-b) / (a+b)) * math.cos(phi)))
        if a - b > 0:
            theta = -theta
        d = b * math.cos(phi - theta) / math.cos(theta)
        return (d, theta)

    # Returns landmarks like QR codes and the goal tower:
    # ((type, ID, distance, angle), ...)
    def getLandmarks(self):
        pass

    def getAbsoluteAngle(self):
        return 0.0

    def getRelativeAngle(self):
        return 0.0

if __name__ == "__main__":
    c.ARD()
    c.DATA()
    c.STATE()
    c.ARD().run()

    while True:
        c.DATA().run()
        c.DATA().log()

        c.STATE().run()
        c.STATE().log()

        time.sleep(.05)
