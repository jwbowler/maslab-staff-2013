import time
import sys
import pid
import arduino
import utils
import * from config

Class Control():

    # The init takes an arduino object
    def __init__(self, arduino):
        self.ard = arduino
        self.roller = arduino.Motor(ard, ROLLER_PINS[0], ROLLER_PINS[1], ROLLER_PINS[2])
        self.rightMotor = arduino.Motor(ard, RIGHT_MOTOR_PINS[0], RIGHT_MOTOR_PINS[2])
        self.leftMotor = arduino.Motor(ard, LEFT_MOTOR_PINS[0], LEFT_MOTOR_PINS[1], LEFT_MOTOR_PINS[2])
        self.helix = arduino.Motor(ard,HELIX_PINS[0], HELIX_PINS[1], HELIX_PINS[2])
        self.ramp = arduino.DigitalOutput(ard, RAMP_SERVO_PIN)
        self.scorer = arduino.DigitalOutput(ard, SCORER_PIN)

        
    # This method turns on and off the roller motor
    # Input:Boolean
    def setRoller(self,switch):
        self.roller.setSpeed(ROLLER_SPEED) 

    # This method turns on and off the helix motor
    # Input:Boolean
    def setHelix(self,switch):
        self.helix.setSpeed(HELIX_SPEED)

    # This method controls the motor that releases the balls
    # Input:Boolean (True when ready to score)
    def setScorer(self,switch):
        value= 127*switch
        self.scorer.setValue(value) 

    # This method actuates the scoring ramp
    #input: angle in degrees from horizontal
    def setRamp(self,angle):
        value= 127*(angle/360)
        self.ramp.setValue(value)

    # This method sets the speed of the left motor
    # Input: int from -1 to 1 inclusive
    def setLeftMotor(self,speed):
        self.leftMotor.setSpeed(speed)

    # This method sets the speed of the right motor
    # Input: int from -1 to 1 inclusive
    def setRightMotor(self,speed):
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
    def bound(input, low, high):
        if input > high:
           return high;
        elif input < low:
           return low
        return input


    # This method rescales an input from 0 to 1 to the oMin and oMax
    # while maintaining sign
    # Input: input and output min and max (absolute)
    def boundAndScale(input, oMin, oMax):
        iMin = 0
        iMax = 1
        thres = .01

        sign = -1 if input < 0 else 1
        input *= sign
        input -= iMin
  
        input *= (oMax-oMin)/(iMax-iMin)
        if input > thresh:
           input += oMin

        input *= sign
        return input

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
