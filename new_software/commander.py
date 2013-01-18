from arduino import Arduino
#from data_collection import DataCollection
import data_collection as d
from state_estimator import StateEstimator
from goal_planning import GoalPlanning
from move_planning import MovePlanning
from control import Control
import config
import signal
import sys


class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

class Commander:
    ard = None
    data = None
    state = None
    goal = None
    move = None
    ctrl = None

        

def ARD():
    if Commander.ard == None:
        Commander.ard = Arduino()
    return Commander.ard

def DATA():
    if Commander.data == None:
        Commander.data = d.DataCollection()
    return Commander.data

def STATE():
    if Commander.state == None:
        Commander.state = StateEstimator()
    return Commander.state

def GOAL():
    if Commander.goal == None:
        Commander.goal = GoalPlanning()
    return Commander.goal

def MOVE():
    if Commander.move == None:
        Commander.move = MovePlanning()
    return Commander.move

def CTRL():
    if Commander.ctrl == None:
        Commander.ctrl = Control()
    return Commander.ctrl

def go():
    signal.signal(signal.SIGALRM, alarm_handler)
    if config.TIME_BEFORE_HALT > 0:
        signal.alarm(TIME_BEFORE_HALT)
    
    ARD()
    DATA()
    STATE()
    GOAL()
    MOVE()
    CTRL()
    ARD().run()

    while True:
        DATA().run()
        STATE().run()
        STATE().log()
        GOAL().run()
        GOAL().log()
        MOVE().run()
        MOVE().log()

def stop():
    DATA().stopVisionThread()
    CTRL().halt()
          
if __name__ == '__main__':
    try:
        go()    
    except (KeyboardInterrupt, Alarm):
        stop()
        sys.exit(0)
