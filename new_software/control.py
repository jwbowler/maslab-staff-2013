import time
import sys
import pid
import arduino
import utils
from config import *

import commander as c


class Control():

    # The init
    def __init__(self):
        self.roller = arduino.Motor(c.ARD(), ROLLER_PINS[0], ROLLER_PINS[1], ROLLER_PINS[2])
        self.rightMotor = arduino.Motor(c.ARD(), RIGHT_MOTOR_PINS[0], RIGHT_MOTOR_PINS[1], RIGHT_MOTOR_PINS[2])
        self.leftMotor = arduino.Motor(c.ARD(), LEFT_MOTOR_PINS[0], LEFT_MOTOR_PINS[1], LEFT_MOTOR_PINS[2])
        self.helix = arduino.Motor(c.ARD(),HELIX_PINS[0], HELIX_PINS[1], HELIX_PINS[2])
        self.ramp = arduino.Motor(c.ARD(), HELIX_PINS[0], HELIX_PINS[1], RAMP_SERVO_PIN)

        self.prevTime = time.time()
        self.prevRight = 0
        self.prevLeft = 0
        self.rightSpeed = 0
        self.leftSpeed = 0
        self.rollerState = False
        self.helixState = False
        self.rampAngle = 0

    def run(self):
        self.roller.setSpeed(-1*ROLLER_SPEED*self.rollerState) 
        self.helix.setSpeed(HELIX_SPEED*self.helixState)
        self.ramp.setAngle(self.rampAngle)

        self.prevLeft = self.accelBound(self.prevLeft, self.leftSpeed)
        l = boundAndScale(self.prevLeft, 8, 127)
        self.leftMotor.setSpeed(l)

        self.prevRight = self.accelBound(self.prevRight, self.rightSpeed)
        r = boundAndScale(self.prevRight, 13, 117)
        self.rightMotor.setSpeed(r)

        self.prevTime = time.time()

    def log(self):
        c.LOG("DRIVE GOAL: " + str((self.leftSpeed,self.rightSpeed)))
        c.LOG("DRIVE ACTUAL: " + str((self.prevLeft,self.prevRight)))
        c.LOG("ROLLER: " + str(self.rollerState))
        c.LOG("HELIX: " + str(self.helixState))
        c.LOG("RAMP: " + str(self.rampAngle))

    def accelBound(self, prevSpeed, goalSpeed):
        delta = goalSpeed - prevSpeed
        maxDelta = ACCEL_LIM * (time.time() - self.prevTime)
        newSpeed = prevSpeed + utils.absBound(delta, maxDelta)
        return utils.absBound(newSpeed, goalSpeed)

    # This method turns on and off the roller motor
    # Input:Boolean
    def setRoller(self,switch):
        self.rollerState = switch

    # This method turns on and off the helix motor
    # Input:Boolean
    def setHelix(self,switch):
        self.helixState = switch

    # This method actuates the scoring ramp
    #input: angle in degrees from vertical
    def setRamp(self,angle):
        self.ramp

    # This method sets the speed of the left motor
    # Input: int from -1 to 1 inclusive
    def setLeftMotor(self,speed):
        self.leftSpeed = speed

    # This method sets the speed of the right motor
    # Input: int from -1 to 1 inclusive
    def setRightMotor(self,speed):
        self.rightSpeed = speed
    

    # This methods calculates motors speeds from a vector
    # Input: speed form -1 to 1 and rotation from -1 to 1(clockwise)
    def setMovement(self,speed, rotation):
        (l,r) = getMotorSpeeds(speed,rotation)
        self.setRightMotor(r)
        self.setLeftMotor(l)

    def halt(self):
        self.setRoller(False)
        self.setHelix(False)
        self.setLeftMotor(0)
        self.setRightMotor(0)
        self.run()
        self.roller.setSpeed(0)
        self.helix.setSpeed(0)
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)

# This method rescales an input from 0 to 1 to the oMin and oMax
# while maintaining sign
# Input: input and output min and max (absolute)
def boundAndScale(value, oMin, oMax):
    iMin = 0
    iMax = 1
    thresh = .01

    sign = -1 if value < 0 else 1
    value *= sign
    value -= iMin

    value *= (oMax-oMin)/(iMax-iMin)
    if value > thresh:
        value += oMin

    if value > oMax:
        value = oMax

    value *= sign
    return int(value)

# This method computes motor speeds given speed and rotation
# Input: velocity and rotation from -1 to 1
# Return: left and right motor speeds from -1 to 1
def getMotorSpeeds(vel, rot):
    r = vel-rot;
    l = vel+rot;

    m = max(abs(r), abs(l))
    if (m > 1):
        r /= m;
        l /= m;

    return (l,r);

if __name__=="__main__":
    c.ARD()
    #c.DATA()
    c.CTRL()
    c.ARD().run()
    
    try:
        '''
        #########################
        c.CTRL().setRoller(True)
        c.CTRL().setHelix(True)
        c.CTRL().setLeftMotor(.0)
        c.CTRL().setRightMotor(.0)
        c.CTRL().setRamp(0)
        print "Running motors..."
        c.CTRL().run()
        time.sleep(5)
        c.CTRL().setLeftMotor(.0)
        c.CTRL().setRightMotor(.0)
        c.CTRL().setRamp(45)
        c.CTRL().run()
        time.sleep(3)
        #c.CTRL().setRamp(90)
        c.CTRL().run()

        #########################
        '''

        c.CTRL().roller.setSpeed(0)

        '''
        for i in xrange(128):
            print i
            c.CTRL().roller.setSpeed(45)
            time.sleep(.2)

        c.CTRL().setHelix(False)
        c.CTRL().setRightMotor(0)
        c.CTRL().setLeftMotor(0)
        time.sleep(1)

        print "Testing Roller"
        c.CTRL().setRoller(True)
        c.CTRL().setHelix(True)
        time.sleep(2)
        c.CTRL().setRoller(False)
        c.CTRL().setHelix(True)

        print "Ramping left"
        #.25
        for i in xrange(60):
            print i
            c.CTRL().leftMotor.setSpeed(i)
            time.sleep(.25)

        c.CTRL().setLeftMotor(0)

        #.225
        print "Ramping right"
        for i in xrange(60):
            print i
            c.CTRL().rightMotor.setSpeed(i)
            time.sleep(.25)

        c.CTRL().setRightMotor(0)

        time.sleep(2)

        print "Testing Helix"
        c.CTRL().setHelix(True)
        time.sleep(3)
        c.CTRL().setHelix(False)

        '''
        print "Testing Ramp"
        for i in xrange(127):
            print i
            c.CTRL().ramp.setSpeed(i)
            time.sleep(.2)

    except KeyboardInterrupt:
        pass

    c.CTRL().halt()
