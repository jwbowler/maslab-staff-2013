from vision import vision_wrapper
import math
import arduino

from config import *

import commander as c

class DataCollection:
    
    # creates data object
    def __init__(self):
        print c.ARD()
        self.initSensors()

    # initializes all the sensors
    def initSensors(self):
        #self.camera = Camera()
        #self.imu = Imu()
        self.encoderPair = EncoderPair(0,0)
        self.irs = [Ir(IR_PINS[i], IR_POSITIONS[i]) for i in xrange(len(IR_PINS))]
        self.ultrasonics = [Ultrasonic(ULTRASONIC_PINS[i], ULTRASONIC_POSITIONS[i]) for i in xrange(len(ULTRASONIC_PINS))]

        self.allSensors = [self.encoderPair]
        self.allSensors.extend(self.irs)
        self.allSensors.extend(self.ultrasonics)
        
        

    # calls run on all of its sensors
    def run(self):
        for sensor in self.allSensors:
            sensor.run()

    def log(self):
        print "~~~DATA~~~"
        #print self.camera
        #print "mine: " + str(self.camera.getMyBalls()) + "theirs: " + str(self.camera.getOpponentBalls())

        #print self.imu

        print "ENC - tics: " + str(self.encoderPair.getTics())

        for ir in self.irs:
            print "IR - position: " + str(ir.getPosition())

        for us in self.ultrasonics:
            print "US - position: " + str(us.getPosition())

        print "~~~DATA~~~\n"



    # return camera object
    def getCamera(self):
        return self.camera

    # return IR object at given index or all IR objects
    # Input: index (0 be the leftmost)
    def getIr(self, index = -1):
        return self.ir if index == -1 else self.ir[index]
        
    # return ultrasonic object at given index or all ultrasonic objects
    # Input: index (0 be the leftmost)
    def getUltrasonic(self, index = -1):
        return self.ultrasonic if index == -1 else self.ultrasonic[index]

    # returns IMU object
    def getIMU(self):
        return self.imu

    # returns encoderPair object (represents both encoders)
    def getEncoderPair(self):
        return self.encoderPair
        
    # halts OpenCV thread
    def stopVisionThread(self):
        self.camera.stopThread()
        
        

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

    def __str__(self):
        print self.__class__.__name__ + " at " + self.timestamp

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
    def stopThread(self):
        self.vision.stop()

        if config.MY_BALLS_ARE_RED:
            self.myBallColor = "RED_BALL"
            self.opponentBallColor = "GREEN_BALL"
        else:
            self.myBallColor = "RED_BALL"
            self.opponentBallColor = "GREEN_BALL"

    # attempts to capture new frame, if vision is not ready: pass
    def run(self):
        isNewFrame = self.vision.update()
        if not isNewFrame:
            return
        self.timestamp = self.vision.getTimestamp()

    # returns (dist, angle) for all my balls
    def getMyBalls(self):
        theirBallIndices = getIndicesByType(self.myBallColor)
        myBalls = [(vision.getX(i), vision.getY(i)) \
                   for i in myBallIndices]
        myBallsConverted = [convCoords(coords) for coords in myBalls]
        return myBallsConverted

    # returns (dist, angle) to all opponent balls
    def getOpponentBalls(self):
        theirBallIndices = getIndicesByType(self.opponentBallColor)
        theirBalls = [(vision.getX(i), vision.getY(i)) \
                      for i in theirBallIndices]
        theirBallsConverted = [convCoords(coords) for coords in theirBalls]
        return theirBallsConverted

    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    def convCoords(x, y):
        angle2obj = (self.angle + self.vfov/2   \
                     - self.vfov*(1.0 * y / self.imHeight))
        d = self.elev * math.tan((math.pi/180) * angle2obj)
        if d < 0:
            d = math.isInf()
        a = (x - (self.imHeight/2.)) * self.hfov / self.imWidth
        return (d, a)

class Ir(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, position):
        self.ardRef = arduino.AnalogInput(c.ARD(), pin)
        (self.radius, self.angle) = position

    def run(self):
        rawValue = self.ardRef.getValue()
        self.distance = self.convertValue(rawValue)

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.radius+self.distance, self.angle)
        
    # takes value from pin and converts it into a distance
    def convertValue(self, value):
        return 0

class Ultrasonic(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, position):
        self.ardRef = arduino.AnalogInput(c.ARD(), pin)
        (self.radius, self.angle) = position

    def run(self):
        rawValue = self.ardRef.getValue()
        self.distance = self.convertValue(rawValue)

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.radius+self.distance, self.angle)
        
    # takes value from pin and converts it into a distance
    def convertValue(self, value):
        return 0

class Imu(Sensor):

    # analog pin
    def __init__(self):
        self.imu = arduino.IMU(c.ARD())

    def run(self):
        (comp0, comp1, self.accelX, self.accelY, self.accelZ) \
            = self.imu.getRawValues()
        self.compassHeading = comp1 * 256 + comp0

    # returns current compass heading
    def getCompassHeading(self):
        return self.compassHeading
        
    def getAccelData(self):
        return (self.accelX, self.accelY, self.accelZ)

class EncoderPair(Sensor):

    # encoder pins
    def __init__(self, leftPin, rightPin):
        pass

    def run(self):
        pass

    # returns totals tics taken (left, right)
    def getTics(self):
        pass

if __name__ == "__main__":
    while True:
        c.DATA().run()
        c.DATA().log()
