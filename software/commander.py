import sys, time, signal

from arduino import Arduino
from vision_interface import VisionInterface, VisionInterfaceDummy
from sensor_interface import SensorInterface, SensorInterfaceDummy
from data_collection import DataCollection
from goal_explore import ExploreGoal
from goal_get_ball import GetBallGoal
from action_follow_wall import FollowWallAction
from action_hunt_ball import HuntBallAction
from action_capture_ball import CaptureBallAction
from action_emergency_reverse import EmergencyReverseAction
from control import Control, ControlDummy

log = False

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

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
    
    global ctl
    if simulateActuators:
        ctl = ControlDummy(ard)
    else:
        ctl = Control(ard)
    
    dc = DataCollection(vi, si)
    
    #actions
    action_fw = FollowWallAction(ctl)
    action_hb = HuntBallAction(ctl)
    action_cb = CaptureBallAction(ctl)
    action_eb = EmergencyReverseAction(ctl)
    action_ss = SpinSearch(ctl)
    
    actionLookup = {                                      \
                    "ACTION_FOLLOW_WALL": action_fw,      \
                    "ACTION_HUNT_BALL": action_hb,        \
                    "ACTION_CAPTURE_BALL": action_cb,     \
                    "ACTION_EMERGENCY_REVERSE": action_eb \
                    "ACTION_ROTATE_IN_PLACE": action_rp   \
                   }
    
    #goals
    goal_ex = ExploreGoal()
    goal_gb = GetBallGoal()
    
    goalLookup = {
                  "GOAL_EXPLORE": goal_ex, \
                  "GOAL_GET_BALL": goal_gb \
                 }
    
    tLast = time.time()
    tAvg = 0
    
    if not (simulateSensors and simulateActuators):
        ard.run()
        
    currentGoal = goal_ex
    
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(10)
    
    while (True):
        data = dc.get()
        if log:
            print "Data: "
            print data
        
            print "Goal: " + currentGoal.getName()

        (nextGoalName, actionName, actionArgs) = currentGoal.step(data)
        currentGoal = goalLookup[nextGoalName]
        
        if log:
            print "Action: " + actionName

        action = actionLookup[actionName]
        if actionArgs == None:
            action.step()
        else:
            action.step(actionArgs)
        
        tCurr = time.time()
        tDiff = tCurr - tLast
        tLast = tCurr
        tAvg = 0.9*tAvg + 0.1*tDiff
        print str(1/tAvg) + " FPS"
        print ""

def three_minute_alarm_callback():
    halt()
    
def halt():
    global ctl
    ctl.drive(0, 0)
    ctl.ballCaptureOff()
        

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, Alarm):
        halt()
        global vi
        del(vi)
        sys.exit(0)


