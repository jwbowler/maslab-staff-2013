import commander as c
import time
import math
from config import *

class StateEstimator:
    # takes data object
    def __init__(self):
        self.data = c.DATA()
        self.startTime = time.time()
        self.towerBase = None
        self.towerMiddle = None
        self.towerTop = None

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
        c.LOG("Adjusted wall distances:")
        c.LOG(self.getWallDistancesAdjusted())
        c.LOG("Collision distance:")
        c.LOG(self.getCollisionDistance())

    def getTimeRemaining(self):
        if TIME_BEFORE_HALT <= 0:
            return -1
        return self.startTime + TIME_BEFORE_HALT - time.time()

    # Called by move_planning after running through the HitButton movement
    def notifyButtonUsed(self):
        self.buttonUsed = True

    def isButtonUsed(self):
        return self.buttonUsed

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
        dist = self.getWallDistancesAdjusted()
        dist = [(p[0]-ROBOT_RADIUS)/math.cos(math.radians(p[1])) for p in dist if abs(p[1]) < 90]
        return min(dist)

    def nearCollision(self):
        return self.getCollisionDistance() < .25

    # Takes two sensor indices to use for wall estimation
    # Returns (distance to wall, angle of wall relative to bot's orientation)
    def getWallPosFrom2Sensors(self, index0, index1):
        sensorList = self.getWallDistancesAdjusted()

        # phi = the angle difference the sensors. index0 -> clockwise -> index1
        phi = abs(sensorList[index0][1] - sensorList[index1][1])

        # measured distances
        a = sensorList[index0][0]
        b = sensorList[index1][0]
        c.LOG("a = " + str(a))
        c.LOG("b = " + str(b))

        # d = calculated distance to robot
        e = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(phi)))
        d = a*b*math.sin(math.radians(phi)) / e
        #c.LOG("e = " + str(e))
        # theta = angle of wall relative to robot
        alpha = math.degrees(math.asin(a * math.sin(math.radians(phi)) / e))
        #c.LOG("alpha = " + str(alpha))
        theta = -alpha + 90 - phi/2

        # offset is zero if sensors are centered at the robot's 9-o'clock, otherwise it corrects theta
        angleOffset = -(sensorList[index0][1] + sensorList[index1][1])/2 - 90
        return (d, theta + angleOffset)

    # Like above, but picks two sensors automatically to use in the calculation
    def getWallRelativePos(self, numSensors):
        sensorList = self.getWallDistancesAdjusted()
        #sensorIndices = sorted(range(numSensors), key = self.getSensorPriority)
        sensorIndices = sorted(range(numSensors), key = lambda i: sensorList[i][0])
        closestSensorIndex = sensorIndices[0]

        # edge cases
        if closestSensorIndex == 0:
            neighborIndex = 1
        elif closestSensorIndex == numSensors - 1:
            neighborIndex = numSensors - 2
        # pick smallest neighbor index
        elif sensorList[closestSensorIndex + 1][0] < sensorList[closestSensorIndex - 1][0]:
            neighborIndex = closestSensorIndex + 1
        else:
            neighborIndex = closestSensorIndex - 1
            
        # Log the priority calculation
        sortedDistances = [sensorList[i][0] for i in sensorIndices]
        sortedMultipliedDistances = [self.getSensorPriority(i) for i in sensorIndices]
        c.LOG("Wall following sensors:")
        c.LOG("closest sensor index = " + str(closestSensorIndex))
        c.LOG("neighbor index = " + str(neighborIndex))

        if sensorList[closestSensorIndex][0] >= .7:
            return (.7, 0)
        if sensorList[neighborIndex][0] >= .7:
            if closestSensorIndex == 0:
                return (.7, 0)
            else:
                return (sensorList[closestSensorIndex][0], -sensorList[closestSensorIndex][1] - 90)

        return self.getWallPosFrom2Sensors(
                min(closestSensorIndex, neighborIndex),
                max(closestSensorIndex, neighborIndex))

    # Returns the priority (smaller is better) of the sensor with the given index,
    # taking into account closeness to front of robot and smallness or distance measurement
    def getSensorPriority(self, index):
        sensorList = self.getWallDistancesAdjusted()
        dist = sensorList[index][0] - ROBOT_RADIUS
        weight = 180 - abs(sensorList[index][1])
        return dist/weight
