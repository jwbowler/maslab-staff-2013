from vision import vision_wrapper
from commander import *
import math
import arduino

class DataCollection:
    
    # creates data object
    def __init__(self):
        pass

    # initializes all the sensors
    def initSensors(self):
        self.camera = Camera()
        
        ir1 = IR(123, 1.4, 0)
        ir2 = IR(456, 1.4, -45)
        ir3 = IR(789, 1.4, -90)
        self.IR = (ir1, ir2, ir3)
        
        self.ultrasonic = None
        self.imu = None
        self.encoders = None

    # calls run on all of its sensors
    def run(self):
        self.camera.run()
        self.ir.run()
        #self.ultrasonic.run()
        #self.imu.run()
        #self.encoders.run()

    # return camera object
    def getCamera(self):
        return self.camera

    # return IR object at given index or all IR objects
    # Input: index (0 be the leftmost)
    def getIR(self, index = -1):
        return self.ir if index == -1 else self.ir[index]
        
    # return ultrasonic object at given index or all ultrasonic objects
    # Input: index (0 be the leftmost)
    def getUltrasonic(self, index = -1):
        return self.ultrasonic if index == -1 else self.ultrasonic[index]

    # returns IMU object
    def getIMU(self):
        return self.imu

    # returns encoders object (represents both encoders)
    def getEncodersPair(self):
        return self.encoders
        
        

class Sensor:

    # updates the timestamp if a measurement was taken
    def run(self):
        raise NotImplementedError

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
        
        self.elev = 0.1
        self.angle = 60. # 0 == pointing down; 90 = pointing forward
        self.imWidth = 640
        self.imHeight = 480
        self.ar = 1. * self.imWidth / self.imHeight
        self.vfov = 50.
        self.hfov = self.ar * self.vfov
    
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
        myBalls = [(vision.getX(i), vision.getY(i)) \
                   for i in myBallIndices]
        myBallsConverted = [convCoords(coords) for coords in myBalls]
        return myBallsConverted

    # returns (dist, angle) to all opponent balls
    def getOpponentBalls(self):
        if Config.MY_BALLS_ARE_RED:
            theirBallIndices = getIndicesByType("GREEN_BALL")
        else:
            theirBallIndices = getIndicesByType("RED_BALL")
        theirBalls = [(vision.getX(i), vision.getY(i)) \
                      for i in theirBallIndices]
        theirBallsConverted = [convCoords(coords) for coords in theirBalls]
        return theirBallsConverted
    
    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    def convCoords(x, y)
        angle2obj = (self.angle + self.vfov/2   \
                     - self.vfov*(1.0 * y / self.imHeight))
        d = self.elev * math.tan((math.pi/180) * angle2obj)
        if d < 0:
            d = math.isInf()
        a = (x - (self.imHeight/2.)) * self.hfov / self.imWidth
        return (d, a)

class IR(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, distance, angle):
        self.ardRef = arduino.analogInput(Commander.ARD, pin)
        self.angle = angle

    def run(self):
        rawValue = self.ardRef.getValue()
        self.distance = convertValue(rawValue)

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.distance, self.angle)
        
    # takes value from pin and converts it into a distance
    def convertValue(value):
        raise NotImplementedError

class Ultrasonic(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, distance, angle):
        self.ardRef = arduino.analogInput(Commander.ARD, pin)

    def run(self):
        rawValue = self.ardRef.getValue()
        self.distance = convertValue(rawValue)

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.distance, self.angle)
        
    # takes value from pin and converts it into a distance
    def convertValue(value):
        raise NotImplementedError

class IMU(Sensor):

    # analog pin
    def __init__(self):
        self.imu = arduino.IMU(Commander.ARD)

    def run(self):
        (comp0, comp1, self.accelX, self.accelY, self.accelZ) \
            = imu.getRawValues()
        self.compassHeading = comp1 * 256 + comp0

    # returns current compass heading
    def getCompassHeading(self):
        return self.compassHeading
        
    def getAccelData(self):
        return (self.accelX, self.accelY, self.accelZ)

class Encoders(Sensor):

    # encoder pins
    def __init__(leftPin, rightPin):
        pass

    def run(self):
        pass

    # returns totals steps taken (left, right)
    def getSteps():
        pass
