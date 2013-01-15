class StateEstimator:

    # takes data object
    def __init__(self):
        pass
    
    # Updates estimated state according to data in Data class
    def run(self):
        pass
        
    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getMyBalls(self):
        pass
        
    # Returns (distance, angle) of nearest ball
    def getMyNearestBall(self):
        pass

    # Returns set of ball distances and angles:
    # ((distance, angle), (distance, angle), ...)
    def getOpponentBalls(self):
        pass
        
    # Returns (distance, angle) of nearest ball
    def getOpponentNearestBall(self):
        pass
    
    # Returns set of wall distances ond angles from all sensors:
    # ((distance, angle), (distance, angle), ...)
    def getWallDistances(self)
        pass
    
    # Returns landmarks like QR codes and the goal tower:
    # ((type, ID, distance, angle), ...)
    def getLandmarks(self)
        pass
