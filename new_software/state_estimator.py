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
        self.towerBase = None
        self.towerTop = None
        self.allBalls = []
        self.nearestBall = None
        self.nearestBallOrGoal = None
        self.nearestNonGoalObj = None
        self.nearestObj = None
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
            self.myBalls = sorted(cam.getMyReachableBalls(), key = lambda obj: obj[0])
            self.opBalls = sorted(cam.getOpReachableBalls(), key = lambda obj: obj[0])
            self.goalWalls = sorted(cam.getReachableGoalWalls(), key = lambda obj: obj[0])
            self.buttons = sorted(cam.getReachableButtons(), key = lambda obj: obj[0])
            self.towerBase = cam.getTowerBase()
            self.towerTop = cam.getTowerTop()
            self.angleAtLastFrame = self.relativeAngle
        elif False:
            shift = self.relativeAngle - self.angleAtLastFrame
            self.myBalls = [(b[0], b[1]+shift) for b in self.myBalls]
            self.opBalls = [(b[0], b[1]+shift) for b in self.opBalls]
            self.goalWalls = [(w[0], w[1]+shift) for w in self.goalWalls]
            self.buttons = [(b[0], b[1]+shift) for b in self.buttons]
            self.tower = (self.tower[0], self.tower[1]+shift)
        self.allBalls = self.myBalls + self.opBalls
        if self.allBalls == []:
            self.nearestBall = None
        else:
            self.nearestBall = min(self.allBalls, key = lambda obj: obj[0])
        if self.allBalls + self.goalWalls == []:
            self.nearestBallOrGoal = None
        else:
            self.nearestBallOrGoal = min(self.allBalls + self.tower, key = lambda obj: obj[0])
        if self.allBalls + self.buttons == []:
            self.nearestNonGoalObj = None
        else:
            self.nearestNonGoalObj = min(self.allBalls + self.buttons, key = lambda obj: obj[0])
        if self.allBalls + self.buttons + self.goalWalls == []:
            self.nearestObj = None
        else:
            self.nearestObj = min(self.allBalls + self.buttons + self.tower, key = lambda obj: obj[0])

        # wallDistRaw = raw data from sensors
        dist = [ir.getPosition() for ir in self.data.getIr()]
        dist.extend([ult.getPosition() for ult in self.data.getUlt()])
        dist = sorted(dist, key = lambda obj: obj[1]) # Sort by angle
        self.wallDistRaw = dist[:]

        # wallDistTimeoutFixed = wallDistRaw after timeout distances are replaced with
        # last known valid distance
        if self.wallDistCorrected != []:
            for i in xrange(len(dist)):
                if dist[i][0] > 1000:
                    dist[i] = self.wallDistCorrected[i]
        self.wallDistTimeoutFixed = dist[:]

        # wallDistLowpass = wallDistTimeoutFixed after blurring
        # not currently used; not sure if correct
        blurAmount = .8
        if self.wallDistLowpass != []:
            for i in xrange(len(dist)):
                corrDist = self.wallDistLowpass[i][0] * blurAmount + dist[i][0] * (1 - blurAmount)
                self.wallDistLowpass[i] = (corrDist, self.wallDistLowpass[1])
        else:
            self.wallDistLowpass = dist[:]
        
        # wallDistOutliersFixed: each distance in the list is the one from wallDistOutliersFixed
        # if it is close enough to the corresponding one from wallDistLowpass, else it is set
        # equal to the corresponding one from wallDistLowpass
        # not currently used; not sure if correct
        errorCutoff = .25
        if self.wallDistOutliersFixed != []:
            for i in xrange(len(dist)):
                if dist[i][0] > (1 + errorCutoff) * self.wallDistLowpass[i][0] \
                 or dist[i][0] < (1 - errorCutoff) * self.wallDistLowpass[i][0]:
                    dist[i] = self.wallDistLowpass[i]
        self.wallDistOutliersFixed = dist[:]

        # set wallDistCorrected
        self.wallDistCorrected = self.wallDistTimeoutFixed[:]
        
        self.timeLastScore = time.time()

    def log(self):
        c.LOG("~~~State Log~~~")

        c.LOG("My Balls")
        c.LOG(self.getMyBalls())

        c.LOG("Opponent Balls")
        c.LOG(self.getOpBalls())

        c.LOG("Buttons")
        c.LOG(self.getButtons())

        c.LOG("Goal Walls")
        c.LOG(self.getGoalWalls())

        c.LOG("Raw Wall Distances")
        c.LOG(self.getRawWallDistances())

        c.LOG("Corrected Wall Dist")
        c.LOG(self.getWallDistances())

        c.LOG("Collision Distance")
        c.LOG(self.getCollisionDistance())

        c.LOG("Near Collision?")
        c.LOG(self.nearCollision())


    def getTimeRemaining(self):
        if TIME_BEFORE_HALT <= 0:
            return 999
        return self.startTime + TIME_BEFORE_HALT - time.time()

    # Called by move_planning after running through the HitButton movement
    def notifyButtonUsed(self):
        self.buttonUsed = True

    def isButtonUsed(self):
        return self.buttonUsed

    # Called by move_planning after running through the Score movement
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
        
        
    # Returns set of ball distances and angles (not behind wall):
    # ((distance, angle), (distance, angle), ...)
    def getMyBalls(self):
        return self.myBalls
        
    # Returns (distance, angle) of nearest ball (not behind wall)
    def getMyNearestBall(self):
        if len(self.myBalls) == 0:
            return None
        return self.myBalls[0]

    # Returns set of ball distances and angles (not behind wall):
    # ((distance, angle), (distance, angle), ...)
    def getOpBalls(self):
        return self.opBalls
        
    # Returns (distance, angle) of nearest ball (not behind wall)
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

    def getTowerBase(self):
        return self.towerBase

    def getTowerTop(self):
        return self.towerTop   

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

    # Returns the nearest ball regardless of color
    def getNearestBall(self):
        return self.nearestBall

    # Returns the nearest object from the combined list of balls and goal walls
    def getNearestBallOrGoal(self):
        return self.nearestBallOrGoal

    # Returns the nearest object that isn't a goal wall
    def getNearestNonGoalObj(self):
        return self.nearestNonGoalObj

    # Returns the nearest object regardless of type
    def getNearestObj(self):
        return self.nearestObj
      
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
        #dist = self.getWallDistances()
        #dist = [p[0]/math.cos(math.radians(p[1])) - ROBOT_RADIUS for p in dist]
        #dist = [d for d in dist if d > 0]
        #return min(dist)
        # temporary:
        # dist = self.getRawWallDistances()[2:]
        # return min(dist)[0]
        # even more temporary:
        return 1000

    def nearCollision(self):
        #return (self.getCollisionDistance() < .12)
        return (self.getCollisionDistance() < .25)

    def getFrontProximity(self):
        # Dependent on a specific sensor configuration. Need to make more general.
        dist = self.getRawWallDistances()
        return dist[3][0]

    # Takes two sensor indices to use for wall estimation
    # Returns (distance to wall, angle of wall relative to bot's orientation)
    def getWallPosFrom2Sensors(self, index0, index1):
        sensorList = self.getWallDistances()
        if index0 < index1:
            sensorA = sensorList[index0]
            sensorB = sensorList[index1]
        else:
            sensorA = sensorList[index1]
            sensorB = sensorList[index0]
        phi = .5 * abs(sensorA[1] - sensorB[1])
        a = sensorA[0]
        b = sensorB[0]
        theta = (180/math.pi) * math.asin(math.sqrt((abs(a-b) / (a+b)) * math.cos(math.pi * phi / 180)))
        if (a > b and theta < 0) or (a < b and theta > 0):
            theta = -theta
        d = b * math.cos((math.pi/180) * (phi - theta)) / math.cos((math.pi/180)*theta)
        # Only works for left-handed wall following until the following line is fixed
        angleOffset = (sensorA[1] + sensorB[1])/2 + 90
        return (d, theta + angleOffset)
        #return (d, theta)

    # Like above, but picks two sensors automatically to use in the calculation
    def getWallRelativePos(self):
        sensorList = self.getWallDistances()
        numSensors = len(sensorList)
        closestSensorIndex = min(range(numSensors), key = lambda i: sensorList[i][0])
        if closestSensorIndex == 0:
            neighborIndex = 1
        elif closestSensorIndex == numSensors - 1:
            neighborIndex = numSensors - 2
        elif sensorList[closestSensorIndex + 1][0] < sensorList[closestSensorIndex - 1][0]:
            neighborIndex = closestSensorIndex + 1
        else:
            neighborIndex = closestSensorIndex - 1
        return self.getWallPosFrom2Sensors(closestSensorIndex, neighborIndex)
    
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
