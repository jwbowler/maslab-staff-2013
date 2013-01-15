Class Control():

    # The init takes an arduino object
    def __init__(arduino):
        pass
  
    # This method turns on and off the roller motor
    # Input:Boolean
    def setRoller(switch):
        pass

    # This method turns on and off the helix motor
    # Input:Boolean
    def setHelix(switch):
        pass

    # This method controls the motor that releases the balls
    # Input:Boolean (True when ready to score)
    def setScorer(switch):
        pass

    # This method actuates the scoring ramp
    #input: angle in degrees from horizontal
    def setRamp(angle):
        pass

    # This method sets the speed of the left motor
    # Input: int from -1 to 1 inclusive
    def setLeftMotor(speed):
        pass

    # This method sets the speed of the right motor
    # Input: int from -1 to 1 inclusive
    def setRightMotor(speed):
        pass
    

    # This methods calculates motors speeds from a vector
    # Input: speed form -1 to 1 and rotation from -1 to 1
    def setMovement(speed, rotation):
        pass



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
