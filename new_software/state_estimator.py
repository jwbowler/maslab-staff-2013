import commander as c
import time
import math
from config import *

class StateEstimator:

    # takes data object
    def __init__(self):
        self.data = c.DATA()
        self.relativeAngle = None
        self.lastImageStamp = None
        self.myBalls = []
        self.opBalls = []
        self.wallDistRaw = []
        self.wallDistTimeoutFixed = []
        self.wallDistLowpass = []
        self.wallDistOutliersFixed = []
        self.wallDistCorrected = []
    
    # Updates estimated state according to data in Data class
    def run(self):
        #self.computeRelativeAngle()

        if c.DATA().getCamera().hasNewFrame():
            self.myBalls = sorted(self.data.getCamera().getMyBalls())
            self.opBalls = sorted(self.data.getCamera().getOpBalls())

            self.angleAtLastFrame = self.relativeAngle
        elif False:
            shift = self.relativeAngle - self.angleAtLastFrame
            self.myBalls = [(b[0], b[1]+shift) for b in self.myBalls]
            self.opBalls = [(b[0], b[1]+shift) for b in self.opBalls]

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

        print "Raw Wall Distances"
        print self.getRawWallDistances()

        print "Corrected Wall Dist"
        print self.getWallDistances()

        print "Collision Distance"
        print self.getCollisionDistance()

        print "Near Collision?"
        print self.nearCollision()

        print "Landmarks"
        print self.getLandmarks()

        print "~~~State Log done~~~"

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
    def getOpBall(self):
        if len(self.opBalls) == 0:
            return None
        return self.opBalls[0]
    
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
