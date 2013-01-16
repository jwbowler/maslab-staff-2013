import time
import sys
import pid
import arduino
from config import *

import commander as c


class Control():

    # The init BLAM
    def __init__(self):
        self.roller = arduino.Motor(c.ARD(), ROLLER_PINS[0], ROLLER_PINS[1], ROLLER_PINS[2])
        self.rightMotor = arduino.Motor(c.ARD(), RIGHT_MOTOR_PINS[0], RIGHT_MOTOR_PINS[2])
        self.leftMotor = arduino.Motor(c.ARD(), LEFT_MOTOR_PINS[0], LEFT_MOTOR_PINS[1], LEFT_MOTOR_PINS[2])
        self.helix = arduino.Motor(c.ARD(),HELIX_PINS[0], HELIX_PINS[1], HELIX_PINS[2])
        self.ramp = arduino.DigitalOutput(c.ARD(), RAMP_SERVO_PIN)
        self.scorer = arduino.DigitalOutput(c.ARD(), SCORER_PIN)

    # This method turns on and off the roller motor
    # Input:Boolean
    def setRoller(self,switch):
        self.roller.setSpeed(ROLLER_SPEED*switch) 

    # This method turns on and off the helix motor
    # Input:Boolean
    def setHelix(self,switch):
        self.helix.setSpeed(HELIX_SPEED*switch)

    # This method controls the motor that releases the balls
    # Input:Boolean (True when ready to score)
    def setScorer(self,switch):
        value= 127*switch
        self.scorer.setValue(value) 

    # This method actuates the scoring ramp
    #input: angle in degrees from vertical
    def setRamp(self,angle):
        value= 127*(angle/180)
        self.ramp.setValue(value)

    # This method sets the speed of the left motor
    # Input: int from -1 to 1 inclusive
    def setLeftMotor(self,speed):
        speed = bound(speed, -1, 1)
        self.leftMotor.setSpeed(speed)

    # This method sets the speed of the right motor
    # Input: int from -1 to 1 inclusive
    def setRightMotor(self,speed):
        speed = bound(speed, -1, 1)
        self.rightMotor.setSpeed(speed)
    

    # This methods calculates motors speeds from a vector
    # Input: speed form -1 to 1 and rotation from -1 to 1(clockwise)
    def setMovement(self,speed, rotation):
        (r,l) = getMotorSpeed(speed,rotation)
        r = boundAndScale(r, -127, 127)
        l = boundAndScale(l, -127, 127)
        self.setRightMotor(r)
        self.setLeftMotor(l)


    # This method bounds an input to low and high
    # Input: input value, low and high limits
    def bound(value, low, high):
        if value > high:
           return high;
        elif value < low:
           return low
        return value


    # This method rescales an input from 0 to 1 to the oMin and oMax
    # while maintaining sign
    # Input: input and output min and max (absolute)
    def boundAndScale(value, oMin, oMax):
        iMin = 0
        iMax = 1
        thres = .01

        sign = -1 if value < 0 else 1
        value *= sign
        value -= iMin
  
        value *= (oMax-oMin)/(iMax-iMin)
        if value > thresh:
           value += oMin

        value *= sign
        return value

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
    control= Control()
    
    print "Testing Left Motor"
    control.setLeftMotor(.3)
    time.sleep(5)
    control.setLeftMotor(0)

    print "Testing Right Motor"
    control.setRightMotor(.3)
    time.sleep(5)
    control.setRightMotor(0)

    print "Testing Helix"
    control.setHelix(True)
    time.sleep(5)
    control.setHelix(False)

    print "Testing Roller"
    control.setRoller(True)
    time.sleep(5)
    control.setRoller(False)

    print "Testing Ramp"
    control.setRamp(90)
    time.sleep(5)
    control.setRamp(0)

    print "Testing Scorer"
    control.setScorer(True)
    time.sleep(5)
    control.setScorer(False)

