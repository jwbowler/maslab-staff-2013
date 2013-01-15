from vision import vision_wrapper

from Commander import *

import math

class DataCollection:
    
    # creates data object
    def __init__(self):
        pass

    # initializes all the sensors
    def initSensors(self):
        pass

    # calls run on all of its sensors
    def run(self):
        pass

    # return camera object
    def getCamera(self):
        return self.camera

    # return ir object at given index or all ir objects
    # Input: index (0 be the leftmost)
    def getIR(self, index = -1):
        return self.IR if index == -1 else self.IR[index]
        
    # return ultrasonic object at given index or all ultrasonic objects
    # Input: index (0 be the leftmost)
    def getUltrasonic(self, index = -1):
        return self.IR if index == -1 else self.IR[index]

    # returns gyro object
    def getGyro(self):
        return self.gyro

    # returns encoders object (represents both encoders)
    def getEncodersPair(self):
        
        

class Sensor:

    # updates the timestamp if a measurement was taken
    def run(self):
        pass

    # return timestamp of last run
    def getTimestamp(self):
        return self.timestamp

    # return time between timestamp and now
    def timeSinceRun(self):
        return time.time() - self.timestamp

class Camera(Sensor):
    
    # creates camera object and starts OpenCV thread
    def __init__(self):
        super(Camera, self).__init__()
        self.vision = vision_wrapper.VisionWrapper()
        self.vision.start()
    
    # stops OpenCV thread
    def __del__(self):
        self.vision.stop()
        super(Camera, self).__del__()

    # attempts to capture new frame, if vision is not ready: pass
    def run(self):
        isNewFrame = self.vision.update()
        if not isNewFrame:
            return
        self.timestamp = self.vision.getTimestamp()

    # returns (dist, angle) for all my balls
    def getMyBalls(self):
        if Config.MY_BALLS_ARE_RED:
            myBallIndices = getIndexesByType("RED_BALL")
        else:
            myBallIndices = getIndexesByType("GREEN_BALL")
        myBalls = [(vision.getX(i), vision.getY(i))
                   for i in myBallIndices]
        myBallsConverted = [convCoords(coords) for coords in myBalls]
        return myBallsConverted

    # returns (dist, angle) to all opponent balls
    def getOpponentBalls(self):
        if Config.MY_BALLS_ARE_RED:
            theirBallIndices = getIndicesByType("GREEN_BALL")
        else:
            theirBallIndices = getIndicesByType("RED_BALL")
        theirBalls = [(vision.getX(i), vision.getY(i))
                      for i in theirBallIndices]
        theirBallsConverted = [convCoords(coords) for coords in theirBalls]
        return theirBallsConverted
    
    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    def convCoords(x, y)
        angle2obj = (self.angle + self.vfov/2
                     - self.vfov*(1.0 * y / self.imHeight))
        d = self.elev * math.tan((math.pi/180) * angle2obj)
        if d < 0:
            d = math.isInf()
        a = (x - (self.imHeight/2.)) * self.hfov / self.imWidth
        return (d, a)

class IR(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, distance, angle):
        pass

    def run(self):
        pass

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        pass

class Ultrasonic(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, distance, angle):
        pass

    def run(self):
        pass

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        pass

class Gyro(Sensor):

    # analog pin
    def __init__(self, pin):
        pass

    def run(self):
        pass

    # returns current angle degrees
    def getAngle(self):
        pass

class Encoders(Sensor):

    # encoder pins
    def __init__(leftPin, rightPin):
        pass

    def run(self):
        pass

    # returns totals steps taken (left, right)
    def getSteps():
        pass
