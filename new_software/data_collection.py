from vislib import vision_wrapper
import math
import time
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
        self.camera = Camera()
        #self.imu = Imu()
        #self.encoderPair = EncoderPair(0,0)
        self.irs = [Ir(IR_PINS[i], IR_POSITIONS[i]) for i in xrange(len(IR_PINS))]
        self.ults= [Ult(ULT_PINS[i], ULT_POSITIONS[i]) for i in xrange(len(ULT_PINS))]
        print [(ULT_PINS[i], ULT_POSITIONS[i]) for i in xrange(len(ULT_PINS))]

        self.allSensors = [self.camera]
        self.allSensors.extend(self.irs)
        self.allSensors.extend(self.ults)
        
        

    # calls run on all of its sensors
    def run(self):
        for sensor in self.allSensors:
            sensor.run()

    def log(self):
        print "~~~DATA~~~"
        print "Camera"
        print "All balls:"
        print "mine: " + str(self.camera.getMyBalls()) + "theirs: " + str(self.camera.getOpBalls())
        print "Reachable balls:"
        print "mine: " + str(self.camera.getMyReachableBalls()) \
              + "theirs: " + str(self.camera.getOpReachableBalls())

        #print self.imu

        #print "ENC - tics: " + str(self.encoderPair.getTics())

        for ir in self.irs:
            print "IR - position: " + str(ir.getPosition()) + " raw: " + str(ir.rawValue)

        for us in self.ults:
            print "US - position: " + str(us.getPosition())

        print "~~~DATA~~~\n"



    # return camera object
    def getCamera(self):
        return self.camera

    # return IR object at given index or all IR objects
    # Input: index (0 be the leftmost)
    def getIr(self, index = -1):
        return self.irs if index == -1 else self.irs[index]
        
    # return ultobject at given index or all ultobjects
    # Input: index (0 be the leftmost)
    def getUlt(self, index = -1):
        return self.ults if index == -1 else self.ults[index]

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
        self.vision = vision_wrapper.VisionWrapper()
        self.vision.start()
        
        self.elev = 0.2
        self.horizOffset = 0.15
        self.angle = 60. # 0 == pointing down; 90 = pointing forward
        self.imWidth = 640
        self.imHeight = 480
        self.ar = 1. * self.imWidth / self.imHeight
        self.vfov = 50.
        self.hfov = self.ar * self.vfov

        if MY_BALLS_ARE_RED:
            self.myBallColor = "RED_BALL"
            self.opBallColor = "GREEN_BALL"
        else:
            self.myBallColor = "GREEN_BALL"
            self.opBallColor = "RED_BALL"

        self.isNewFrame = False

    # stops OpenCV thread
    def stopThread(self):
        print "stopThread"
        self.vision.stop()

    # attempts to capture new frame, if vision is not ready: pass
    def run(self):
        self.isNewFrame = self.vision.update()
        if self.isNewFrame:
            self.timestamp = self.vision.getTimestamp()

    def hasNewFrame(self):
        return self.isNewFrame

    def getObjsOfType(self, objType, objHeight):
        objIndices = self.vision.getIndicesByType(objType)
        objs = [(self.vision.getX(i), self.vision.getY(i)) \
                      for i in objIndices]
        objsConverted = [self.convCoords(coords, objHeight) for coords in objs]
        return objsConverted

    def getReachableObjsOfType(self, objType, objHeight):
        objIndices = self.vision.getIndicesByType(objType)
        objs = [(self.vision.getX(i), self.vision.getY(i)) \
                      for i in objIndices if not self.vision.getIsBehindWall(i)]
        objsConverted = [self.convCoords(coords, objHeight) for coords in objs]
        return objsConverted 

    # returns (dist, angle) to all my balls
    def getMyBalls(self):
        return self.getObjsOfType(self.myBallColor, BALL_RADIUS)

    # returns (dist, angle) to all opponent balls
    def getOpBalls(self):
        return self.getObjsOfType(self.opBallColor, BALL_RADIUS) 

    # returns (dist, angle) to all my balls that aren't behind walls
    def getMyReachableBalls(self):
        return self.getReachableObjsOfType(self.myBallColor, BALL_RADIUS) 

    # returns (dist, angle) to all opponent balls that aren't behind walls
    def getOpReachableBalls(self):
        return self.getReachableObjsOfType(self.opBallColor, BALL_RADIUS)

    def getGoalWalls(self):
        return self.getObjsOfType("YELLOW_WALL", YELLOW_WALL_CENTER_HEIGHT/2)

    def getReachableGoalWalls(self):
        return self.getReachableObjsOfType("YELLOW_WALL", YELLOW_WALL_CENTER_HEIGHT/2)

    def getButtons(self):
        return self.getObjsOfType("CYAN_BUTTON", BUTTON_CENTER_HEIGHT)

    def getReachableButtons(self):
        return self.getReachableObjsOfType("CYAN_BUTTON", BUTTON_CENTER_HEIGHT)

    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    def convCoords(self, (x, y), objHeight):
        angle2obj = (self.angle + self.vfov/2   \
                     - self.vfov*(1.0 * y / self.imHeight))
        d = (self.elev - objHeight) * math.tan((math.pi/180) * angle2obj)
        if d < 0:
            d = 1000000
        a = (x - (self.imWidth/2.)) * self.hfov / self.imWidth
        #a -= 10  # fudge factor
        return (d, a)

class Ir(Sensor):

    # analog pin and position relative bot center
    def __init__(self, pin, position):
        self.ardRef = arduino.AnalogInput(c.ARD(), pin)
        (self.radius, self.angle) = position
        self.distance = -1

    def run(self):
        self.rawValue = self.ardRef.getValue()
        self.distance = self.convertValue(self.rawValue)

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.radius+self.distance, self.angle)
        
    # takes value from pin and converts it into a distance
    def convertValue(self, value):
        if value == None:
            return 1000

        #yay excel
        x = math.log(value, 10)
        return 10**(3.1307*x**2 - 19.329*x + 30.707)




class Ult(Sensor):

    # analog pin and position relative bot center
    def __init__(self, (trig, echo), position):
        self.ardRef = arduino.Ult(c.ARD(), trig, echo)
        (self.radius, self.angle) = position
        self.distance = -1

    def run(self):
        self.rawValue  = self.ardRef.getRawValue()

    # returns (distance, angle) from center of bot, None if failing
    def getPosition(self):
        return (self.radius+self.getValMeters(), self.angle)

    def getValMeters(self):
        val = self.rawValue
        #used to be 29*2 
        return 1000 if val == None or val == 0 else (val/5359.2)
        
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
    c.ARD()
    c.DATA()
    c.CTRL()
    c.ARD().run()

    try:
        while True:
            c.DATA().run()
            c.DATA().log()
            time.sleep(.5)
    except KeyboardInterrupt:
        print "Interrupting"
        c.CTRL().halt()
        c.DATA().stopVisionThread()
