import sys

import arduino
import vision_interface
import sensor_interface
import data_collection 
import state_machine
import state_follow_wall
import state_hunt_ball
import control

def main():

    ard = arduino.Arduino()
    vi = VisionInterface()
    si = SensorInterface(ard)
    dc = DataCollection(vi, si)
    ctl = Control()
    # FollowWallState only takes an Arduino object for now; will take SensorWrapper
    stateDict = { \
                 "FOLLOW_WALL", FollowWallState(ard, ctl), \
                 "HUNT_BALL", HuntBallState(ctl), \
                 "HALT", HaltState(ctl) \
                }
    global sm
    sm = StateMachine(dc, sd)
    #TODO: Register alarm callback
    
    while (True):
        sm.step()

def three_minute_alarm_callback():
    global sm
    sm.halt()
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)


