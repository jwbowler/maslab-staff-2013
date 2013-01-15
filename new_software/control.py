Class Control():

    # The init takes an arduino object
    def __init__(arduino):
  
    # This method turns on and off the roller motor
    # Input:Boolean
    def setRoller(switch):

    # This method turns on and off the helix motor
    # Input:Boolean
    def setHelix(switch):

    # This method controls the motor that releases the balls
    # Input:Boolean (True when ready to score)
    def setScorer(switch):

    # This method actuates the scoring ramp
    #input: angle in degrees from horizontal
    def setRamp(angle):

    # This method sets the speed of the left motor
    # Input: int from -1 to 1 inclusive
    def setLeftMotor(speed):

    # This method sets the speed of the right motor
    # Input: int from -1 to 1 inclusive
    def setRightMotor(speed):



    def bound(val, low, high):
        if val > high:
           return high;
        elif val < low:
           return low
        return val


    def boundAndScale(val, iMin, iMax, thresh,  oMin, oMax):
        sign = -1 if val < 0 else 1
        val *= sign
        val -= iMin
  
        val *= (oMax-oMin)/(iMax-iMin)
        if val > thresh:
           val += oMin

        val *= sign
        return val

    def getMotorSpeeds(vel, rot):
        r = vel-rot;
        l = vel+rot;

        m = max(abs(r), abs(l))
        if (m > 1):
            r /= m;
            l /= m;

        return (r,l);

