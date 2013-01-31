from arduino import Arduino
from start import Start
#from data_collection import DataCollection
import data_collection as d
from state_estimator import StateEstimator
from goal_planning import GoalPlanning
from move_planning import MovePlanning
from control import Control
from config import *
import signal
import sys
import time


class Commander:
    ard = None
    start = None
    data = None
    state = None
    goal = None
    move = None
    ctrl = None
    logTime = 0
    logging = False
    frameCount = 0
    myBallsAreRed = True

def MY_BALLS_ARE_RED():
    return Commander.myBallsAreRed

def ARD():
    if Commander.ard == None:
        Commander.ard = Arduino()
    return Commander.ard

def START():
    if Commander.start == None:
        Commander.start = Start()
    return Commander.start

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

def LOG(str):
    if Commander.logging:
        print str

def FRAME_START():
    t = time.time()

    if Commander.logging:
        Commander.logging = False
        print ""

    if t > Commander.logTime:
        Commander.logTime = t + LOG_FREQUENCY
        Commander.logging = True
        print "~~~ FRAME " + str(Commander.frameCount) + " ~~~"

    Commander.frameCount += 1

def go():
    ARD()
    DATA()
    STATE()
    GOAL()
    MOVE()
    CTRL()
    START()
    ARD().run()

    while True:
        Commander.myBallsAreRed = START().poll()
        if Commander.myBallsAreRed is not None:
            break
        time.sleep(.01)

    print "Are my balls red?"
    print Commander.myBallsAreRed
    
    while True:
        FRAME_START()
        DATA().run()
        DATA().log()
        STATE().run()
        STATE().log()
        GOAL().run()
        GOAL().log()
        MOVE().run()
        MOVE().log()
        CTRL().run()
        CTRL().log()

def stop():
    CTRL().halt()
    DATA().stopVisionThread()
    
