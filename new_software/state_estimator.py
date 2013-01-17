import commander as c
import time
import math
from config import *

class StateEstimator:

    # takes data object
    def __init__(self):
        self.data = c.DATA()
    
    # Updates estimated state according to data in Data class
    def run(self):
        self.computeRelativeAngle()
        self.myBalls = self.data.getCamera().getMyBalls()
        self.myBalls = sorted(self.myBalls, lambda ball: ball[0])
        self.opponentBalls = self.data.getCamera().getOpponentBalls()
        self.opponentBalls = sorted(self.opponentBalls, lambda ball: ball[0])

    def log(self):
        print "~~~State Log~~~"

        print "My Balls"
        print self.getMyBalls()

        print "Opponent Balls"
        print self.getOpponentBalls()

        print "Wall Distances"
        print self.getWallDistances()

        print "Collision Distance"
        print self.getCollisionDistance()

        print "Landmarks"
        print self.getLandmarks()

        print "~~~State Log done~~~"

        
    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getMyBalls(self):
        return self.myBalls
        
    # Returns (distance, angle) of nearest ball
    def getMyNearestBall(self):
        return self.myBalls[0]

    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getOpponentBalls(self):
        return self.opponentBalls
        
    # Returns (distance, angle) of nearest ball
    def getOpponentNearestBall(self):
        return self.opponentBalls[0]
    
    # Returns set of wall distances ond angles from all sensors:
    # ((distance, angle), (distance, angle), ...)
    def getWallDistances(self):
        return [ir.getPosition() for ir in self.data.getIr()]
        
    # Returns the forward distance that the robot can travel
    # before it hits a wall
    def getCollisionDistance(self):
        dist = [ir.getPosition() for ir in self.data.getIr()]
        dist = [p[0]/math.cos(math.radians(p[1])) - ROBOT_RADIUS for p in dist]
        return min(dist)


    def nearCollision(self):
        return (self.getCollisionDistance() < .05)
    
    # Returns landmarks like QR codes and the goal tower:
    # ((type, ID, distance, angle), ...)
    def getLandmarks(self):
        pass

    def getAbsoluteAngle(self):
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

        time.sleep(.5)
