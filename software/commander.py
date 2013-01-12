import sys, time

from arduino import Arduino
from vision_interface import VisionInterface, VisionInterfaceDummy
from sensor_interface import SensorInterface, SensorInterfaceDummy
from data_collection import DataCollection
from state_machine import StateMachine, HaltState
from state_follow_wall import FollowWallState
from state_hunt_ball import HuntBallState
from control import Control, ControlDummy

def main():

    simulateCamera = False
    simulateSensors = True
    simulateActuators = False
    
    ard = Arduino()
    
    global vi
    if simulateCamera:
        vi = VisionInterfaceDummy()
    else:
        vi = VisionInterface()
        
    if simulateSensors:
        si = SensorInterfaceDummy(ard)
    else:
        si = SensorInterface(ard)
        
    if simulateActuators:
        ctl = ControlDummy(ard)
    else:
        ctl = Control(ard)
    
    dc = DataCollection(vi, si)
    
    # FollowWallState only takes an Arduino object for now; will take SensorWrapper
    stateDict = { \
                 "FOLLOW_WALL": FollowWallState(ard, ctl), \
                 "HUNT_BALL":   HuntBallState(ctl),        \
                 "HALT":        HaltState(ctl)             \
                }
    global sm
    sm = StateMachine(dc, stateDict)
    #TODO: Register alarm callback
    
    tLast = time.time()
    tAvg = 0
    
    if not (simulateSensors and simulateActuators):
        ard.run()
  
    while (True):
        sm.step()
        #ctl.drive(20, 127)
        
        tCurr = time.time()
        tDiff = tCurr - tLast
        tLast = tCurr
        tAvg = 0.9*tAvg + 0.1*tDiff
        print str(1/tAvg) + " FPS"
        print ""

def three_minute_alarm_callback():
    global sm
    sm.halt()
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        global sm
        sm.halt()
        global vi
        del(vi)
        sys.exit(0)


