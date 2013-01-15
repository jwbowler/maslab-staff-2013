class StateEstimator:

    # takes data object
    def __init__(self):
        self.data = Commander.DATA
    
    # Updates estimated state according to data in Data class
    def run(self):
        self.myBalls = self.data.getCamera().getMyBalls()
        self.myBalls = sorted(myBalls, lambda ball: ball[0])
        self.opponentBalls = self.data.getCamera().getOpponentBalls()
        self.opponentBalls = sorted(myBalls, lambda ball: ball[0])
        
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
        return [ir.getPosition for ir in self.data.getIR()]
        
    # Returns the forward distance that the robot can travel
    # before it hits a wall
    def getCollisionDistance(self):
        headOnDist = self.data.getIR(0) - Config.ROBOT_RADIUS
        diagDist = self.data.getIR(1) - Config.ROBOT_RADIUS
        diagCollisionDist = diagDist * math.sqrt(2) \
                            - Config.ROBOT_RADIUS / math.sqrt(2) 
        return min(headOnDist, diagCollisionDist)
    
    # Returns landmarks like QR codes and the goal tower:
    # ((type, ID, distance, angle), ...)
    def getLandmarks(self)
        pass
