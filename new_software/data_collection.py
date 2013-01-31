from vislib import vision_wrapper
import math
import time
import arduino

from config import *

import commander as c

class DataCollection:
    # creates data object
    def __init__(self):
        self.initSensors()

    # initializes all the sensors
    def initSensors(self):
        self.camera = Camera()
        #self.imu = Imu()
        #self.encoderPair = EncoderPair(0,0)
        self.irs = [Ir(IR_PINS[i], IR_POSITIONS[i]) for i in xrange(len(IR_PINS))]
        self.ults= [Ult(ULT_PINS[i], ULT_POSITIONS[i]) for i in xrange(len(ULT_PINS))]
        self.allSensors = [self.camera]
        self.allSensors.extend(self.irs)
        self.allSensors.extend(self.ults)
        
        

    # calls run on all of its sensors
    def run(self):
        for sensor in self.allSensors:
            sensor.run()

    def log(self):
        c.LOG("~~~DATA~~~")
        c.LOG("Camera")
        c.LOG("All balls:")
        c.LOG("mine: " + str(self.camera.getMyBalls()) + "theirs: " + str(self.camera.getOpBalls()))
        c.LOG("Reachable balls:")
        c.LOG("mine: " + str(self.camera.getMyReachableBalls()) + "theirs: " + str(self.camera.getOpReachableBalls()))
        c.LOG("Goal walls: " + str(self.camera.getGoalWalls()))
        c.LOG("Reachable goal walls: " + str(self.camera.getReachableGoalWalls()))
        c.LOG("Buttons: " + str(self.camera.getButtons()))
        c.LOG("Reachable buttons: " + str(self.camera.getReachableButtons()))
        c.LOG("Tower base (bottom): " + str(self.camera.getTowerBase_Bottom()))
        c.LOG("Tower base (center): " + str(self.camera.getTowerBase_Center()))
        c.LOG("Tower middle (bottom): " + str(self.camera.getTowerMiddle_Bottom()))
        c.LOG("Tower middle (center): " + str(self.camera.getTowerMiddle_Center()))
        c.LOG("Tower top (bottom): " + str(self.camera.getTowerTop_Bottom()))
        c.LOG("Tower top (center): " + str(self.camera.getTowerTop_Center()))

        #print self.imu

        #print "ENC - tics: " + str(self.encoderPair.getTics())

        for ir in self.irs:
            c.LOG("IR - position: " + str(ir.getPosition()) + " raw: " + str(ir.rawValue))

        for us in self.ults:
            c.LOG("US - position: " + str(us.getPosition()))

        c.LOG("~~~DATA~~~\n")



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
        return self.__class__.__name__ + " at " + self.timestamp

class Camera(Sensor):
    # creates camera object and starts OpenCV thread
    def __init__(self):
        self.vision = vision_wrapper.VisionWrapper()
        self.vision.start()
        
        self.elev = 0.343
        self.horizOffset = 0.0
        self.angle = 65.1 # 0 == pointing down; 90 = pointing forward
        self.imWidth = 640
        self.imHeight = 480
        self.ar = 1. * self.imWidth / self.imHeight
        self.vfov = 49.8
        self.hfov = self.ar * self.vfov

        if c.MY_BALLS_ARE_RED:
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

    # Possible object type strings:
    # "RED_BALL", "GREEN_BALL", "YELLOW_WALL", "CYAN_BUTTON"

    # Takes a string representing an objects type (see list above)
    # and a number representing the height of the object's center
    # above the ground (used to calculate distance).
    # Returns a list: [(dist, angle), (dist, angle), ...]
    def getObjsOfType(self, type, objHeight, useBottom=False):
        objIndices = self.vision.getIndicesByType(type)
        if useBottom:
            objs = [(self.vision.getXBottom(i), self.vision.getYBottom(i)) \
                          for i in objIndices]
        else:
            objs = [(self.vision.getXCenter(i), self.vision.getYCenter(i)) \
                          for i in objIndices]
        objsConverted = [self.convCoords(coords, objHeight) for coords in objs]
        return objsConverted

    # Like above, but only returns objects that aren't behind walls
    def getReachableObjsOfType(self, type, objHeight, useBottom=False):
        objIndices = self.vision.getIndicesByType(type)
        if useBottom:
            objs = [(self.vision.getXBottom(i), self.vision.getYBottom(i)) \
                          for i in objIndices if not self.vision.getIsBehindWall(i)]
        else:
            objs = [(self.vision.getXCenter(i), self.vision.getYCenter(i)) \
                          for i in objIndices if not self.vision.getIsBehindWall(i)]
        objsConverted = [self.convCoords(coords, objHeight) for coords in objs]
        return objsConverted 

    def getBiggestObjOfType(self, type, objHeight, useBottom=False):
        objIndices = self.vision.getIndicesByType(type)
        if objIndices == []:
            return None
        index = max(objIndices, key = lambda i: self.vision.getWeight(i))
        if useBottom:
            coords = (self.vision.getXBottom(index), self.vision.getYBottom(index))
        else:
            coords = (self.vision.getXCenter(index), self.vision.getYCenter(index))
        out = self.convCoords(coords, objHeight)
        return out

    def getBiggestReachableObjOfType(self, type, objHeight, useBottom=False):
        objIndices = self.vision.getIndicesByType(type)
        objIndices = [i for i in objIndices if not self.vision.getIsBehindWall(i)]
        if objIndices == []:
            return None
        index = max(objIndices, key = lambda i: self.vision.getWeight(i))
        if useBottom:
            coords = (self.vision.getXBottom(index), self.vision.getYBottom(index))
        else:
            coords = (self.vision.getXCenter(index), self.vision.getYCenter(index))
        out = self.convCoords(coords, objHeight)
        return out

    # returns (dist, angle) to all my balls
    def getMyBalls(self):
        return self.getObjsOfType(self.myBallColor, BALL_RADIUS)
        #return self.getObjsOfType(self.myBallColor, 0)

    # returns (dist, angle) to all opponent balls
    def getOpBalls(self):
        return self.getObjsOfType(self.opBallColor, BALL_RADIUS) 
        #return self.getObjsOfType(self.opBallColor, 0) 

    # returns (dist, angle) to all my balls that aren't behind walls
    def getMyReachableBalls(self):
        return self.getReachableObjsOfType(self.myBallColor, BALL_RADIUS) 
        #return self.getReachableObjsOfType(self.myBallColor, 0) 

    # returns (dist, angle) to all opponent balls that aren't behind walls
    def getOpReachableBalls(self):
        return self.getReachableObjsOfType(self.opBallColor, BALL_RADIUS)
        #return self.getReachableObjsOfType(self.opBallColor, 0)

    def getGoalWalls(self):
        return self.getObjsOfType("YELLOW_WALL", YELLOW_WALL_CENTER_HEIGHT)
        #return self.getObjsOfType("YELLOW_WALL", 0)

    def getReachableGoalWalls(self):
        return self.getReachableObjsOfType("YELLOW_WALL", YELLOW_WALL_CENTER_HEIGHT)
        #return self.getReachableObjsOfType("YELLOW_WALL", 0)

    def getButtons(self):
        return self.getObjsOfType("CYAN_BUTTON", BUTTON_CENTER_HEIGHT)

    def getReachableButtons(self):
        return self.getReachableObjsOfType("CYAN_BUTTON", BUTTON_CENTER_HEIGHT)

    def getTowerBase_Bottom(self):
        return self.getBiggestObjOfType("PURPLE_GOAL", 0, True)

    def getTowerBase_Center(self):
        return self.getBiggestObjOfType("PURPLE_GOAL", 0, False)

    def getTowerMiddle_Bottom(self):
        return self.getBiggestObjOfType("YELLOW_WALL", TOWER_MIDDLE_BOTTOM_HEIGHT, True)

    def getTowerMiddle_Center(self):
        return self.getBiggestObjOfType("YELLOW_WALL", TOWER_MIDDLE_BOTTOM_HEIGHT, False)

    def getTowerTop_Bottom(self):
        return self.getBiggestObjOfType("BLUE_GOAL", TOWER_TOP_BOTTOM_HEIGHT, True)

    def getTowerTop_Center(self):
        return self.getBiggestObjOfType("BLUE_GOAL", TOWER_TOP_BOTTOM_HEIGHT, False)

    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    # returns (dist, angle) given x and y pixel coordinates (from upper left)
    def convCoords(self, (x, y), objHeight):
        angle2obj = (self.angle + self.vfov/2   \
                     - self.vfov*(1.0 * y / self.imHeight))
        d = (self.elev - objHeight) * math.tan((math.pi/180) * angle2obj)
        if d < 0:
            d = 1000000
        a = (x - (self.imWidth/2.)) * self.hfov / self.imWidth
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
        self.rawValue = None

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
            c.FRAME_START()
            c.DATA().run()
            c.DATA().log()
            #c.CTRL().setMovement(0.2, 0)
            time.sleep(.1)
    except KeyboardInterrupt:
        print "Interrupting"
        c.CTRL().halt()
        c.DATA().stopVisionThread()
