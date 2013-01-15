class DataCollection:
    
    # creates data object
    def __init__(self, ard):
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
        pass

    # return time between timestamp and now
    def timeSinceRun(self):
        pass

class Camera(Sensor):
    
    # creates camera
    def __init__(self):
        pass

    # attempts to capture new frame, if vision is not ready: pass
    def run(self):
        pass

    # returns (angle, dist) for all my balls
    def getMyBalls(self):
        pass

    # returns (angle, dist) to all opponent balls
    def getOpponentBalls(self):
        pass

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
