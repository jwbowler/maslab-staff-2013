import math

class Test:

    def getWallDistances(self):
        return [(9, -91), (90, -89)]

    # Takes two sensor indices to use for wall estimation
    # Returns (distance to wall, angle of wall relative to bot's orientation)
    def getWallPosFrom2Sensors(self, index0, index1):
        sensorList = self.getWallDistances()

        # phi = the angle difference the sensors. index0 -> clockwise -> index1
        phi = abs(sensorList[index0][1] - sensorList[index1][1])

        # measured distances
        a = sensorList[index0][0]
        b = sensorList[index1][0]

        # d = calculated distance to robot
        # theta = angle of wall relative to robot. will return positive
        # unless the sensors are >180 degrees apart, measured clockwise from index0 to index1
        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(phi)))
        print c
        alpha = math.degrees(math.asin(a * math.sin(math.radians(phi)) / c))
        print alpha
        d = a*b*math.sin(math.radians(phi)) / c
        theta = alpha - 90 + phi/2

        # sets sign of theta: negative means the robot will hit the wall
        if (a > b and theta > 0) or (a < b and theta < 0):
            theta = -theta

        # offset is zero if sensors are centered at the robot's 9-o'clock, otherwise it corrects theta
        angleOffset = -(sensorList[index0][1] + sensorList[index1][1])/2 - 90
        return (d, theta + angleOffset)

    # Like above, but picks two sensors automatically to use in the calculation
    def getWallRelativePos(self, numSensors):
        sensorList = self.getWallDistances()
        sensorIndices = sorted(range(numSensors), key = getSensorPriority)
        closestSensorIndex = sensorIndices[0]

        # edge cases
        if closestSensorIndex == 0:
            neighborIndex = 1
        elif closestSensorIndex == numSensors - 1:
            neighborIndex = numSensors - 2
        # pick smallest neighbor index
        elif sensorList[closestSensorIndex + 1][0] < sensorList[closestSensorIndex - 1][0]:
            neighborIndex = closestSensorIndex + 1
        else:
            neighborIndex = closestSensorIndex - 1
            
        # Log the priority calculation
        sortedDistances = [sensorList[i][0] for i in sensorIndices]
        sortedMultipliedDistances = [getSensorPriority(i) for i in sensorIndices]
        c.LOG("Wall following sensors:")
        c.LOG("closest sensor index = " + str(closestSensorIndex))
        c.LOG("neighbor index = " + str(neighborIndex))

        return self.getWallPosFrom2Sensors(
                min(closestSensorIndex, neighborIndex),
                max(closestSensorIndex, neighborIndex))

    # Returns the priority (smaller is better) of the sensor with the given index,
    # taking into account closeness to front of robot and smallness or distance measurement
    def getSensorPriority(self, index):
        dist = sensorList[i][0] - ROBOT_RADIUS
        weight = 180 - abs(sensorList[i][1])
        return dist/weight
        
if __name__ == '__main__':
    t = Test()
    print t.getWallPosFrom2Sensors(0, 1)
