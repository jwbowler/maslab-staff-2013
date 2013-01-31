import commander as c
import time
import math
from config import *

class StateEstimator:
    # takes data object
    def __init__(self):
        self.data = c.DATA()
        self.startTime = time.time()

    # Updates estimated state according to data in Data class
    def run(self):
        #self.computeRelativeAngle()
        cam = self.data.getCamera()
        if cam.hasNewFrame():
            self.loadFrame()

    def loadFrame(self):
        if cam.getTowerBase_Bottom() is not None:
            self.towerBase = (cam.getTowerBase_Bottom()[0], cam.getTowerBase_Center()[1])
        else:
            self.towerBase = None
        if cam.getTowerMiddle_Bottom() is not None:
            self.towerMiddle = (cam.getTowerMiddle_Bottom()[0], cam.getTowerMiddle_Center()[1])
        else:
            self.towerMiddle = None
        if cam.getTowerTop_Bottom() is not None:
            self.towerTop = (cam.getTowerTop_Bottom()[0], cam.getTowerTop_Center()[1])
        else:
            self.towerTop = None
        self.angleAtLastFrame = self.relativeAngle


    def log(self):
        c.LOG("~~~State Log~~~")

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

    # Returns set of ball distances and angles (not behind wall):
    # ((distance, angle), (distance, angle), ...)
    def getMyBalls(self):
        return sorted(cam.getMyReachableBalls())
        
    # Returns (distance, angle) of nearest ball (not behind wall)
    def getMyNearestBall(self):
        balls = self.getMyBalls()
        return balls[0] if len(balls) > 0 else None

    # Returns set of ball distances and angles (not behind wall):
    # ((distance, angle), (distance, angle), ...)
    def getOpBalls(self):
        return sorted(cam.getOpReachableBalls())
        
    # Returns (distance, angle) of nearest ball (not behind wall)
    def getOpNearestBall(self):
        balls = self.getOpBalls()
        return balls[0] if len(balls) > 0 else None

    def getGoalWalls(self):
        return sorted(cam.getReachableGoalWalls())
        
    def getNearestGoalWall(self):
        walls = self.getGoalWalls()
        return balls[0] if len(balls) > 0 else None

    def getButton(self):
        buttons = sorted(cam.getReachableButtons())
        return buttons[0] if len(buttons) > 0 else None
        
    def getTowerBase(self):
        return self.towerBase

    def getTowerMiddle(self):
        return self.towerMiddle

    def getTowerTop(self):
        return self.towerTop   

    def getObjType(self, obj):
        if obj in self.myBalls:
            if c.MY_BALLS_ARE_RED():
                return "RED_BALL"
            else:
                return "GREEN_BALL"
        if obj in self.opBalls:
            if c.MY_BALLS_ARE_RED():
                return "GREEN_BALL"
            else:
                return "RED_BALL"
        if obj in self.goalWalls:
            return "YELLOW_WALL"
        if obj in self.buttons:
            return "CYAN_BUTTON"
        if obj == self.towerBase:
            return "PURPLE_GOAL"
        if obj == self.towerMiddle:
            return "YELLOW_WALL"
        if obj == self.towerTop:
            return "BLUE_GOAL"
        else:
            return None

    # Returns the nearest ball regardless of color
    def getNearestBall(self):
        allBalls = sorted(self.getMyBalls() + self.getOpBalls())
        return allBalls[0] if len(allBalls) > 0 else None

    # Returns fully corrected set of wall distances ond angles from all sensors:
    # ((distance, angle), (distance, angle), ...)
    def getWallDistancesAdjusted(self):
        dist = self.getRawWallDistances()
        for i in xrange(len(dist)):
            if dist[i][0] > 1000:
                dist[i] = (.7, dist[i][1])
        return dist

    # Returns wall distances without any corrections
    def getRawWallDistances(self):
        dist = [ir.getPosition() for ir in self.data.getIr()]
        dist.extend([ult.getPosition() for ult in self.data.getUlt()])
        dist = sorted(dist, key = lambda obj: obj[1]) # Sort by angle
        return dist

    # Returns the forward distance that the robot can travel
    # before it hits a wall
    def getCollisionDistance(self):
        dist = self.getWallDistances()
        dist = [(p[0]-ROBOT_RADIUS)/math.cos(math.radians(p[1])) - ROBOT_RADIUS for p in dist if abs(p[1]) < 90]
        return min(dist)

    def nearCollision(self):
        return self.getCollisionDistance() < .25

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
        if (a > b and theta > 0) or (a < b and theta < 0):
            theta = -theta
        d = b * math.cos((math.pi/180) * (phi - theta)) / math.cos((math.pi/180)*theta)
        # Only works for left-handed wall following until the following line is fixed
        angleOffset = -(sensorA[1] + sensorB[1])/2 - 90
        c.LOG("offset angle = " + str(angleOffset))
        return (d, theta + angleOffset)
        #return (d, theta)

    # Like above, but picks two sensors automatically to use in the calculation
    def getWallRelativePos(self, numSensors):
        sensorList = self.getWallDistances()
        sensorIndices = sorted(range(numSensors), \
                                 key = lambda i: (sensorList[i][0] - ROBOT_RADIUS) / (180 - abs(sensorList[i][1])))
        sortedDistances = [sensorList[i][0] for i in sensorIndices]
        sortedMultipliedDistances = [(sensorList[i][0] - ROBOT_RADIUS) / (180 - abs(sensorList[i][1])) for i in sensorIndices]
        closestSensorIndex = sensorIndices[0]
        if closestSensorIndex == 0:
            neighborIndex = 1
        elif closestSensorIndex == numSensors - 1:
            neighborIndex = numSensors - 2
        elif sensorList[closestSensorIndex + 1][0] < sensorList[closestSensorIndex - 1][0]:
            neighborIndex = closestSensorIndex + 1
        else:
            neighborIndex = closestSensorIndex - 1
        c.LOG("Wall following sensors:")
        c.LOG("closest sensor index = " + str(closestSensorIndex))
        c.LOG("neighbor index = " + str(neighborIndex))
        return self.getWallPosFrom2Sensors(closestSensorIndex, neighborIndex)
