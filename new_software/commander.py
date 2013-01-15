from arduino import Arduino
from data_collection import DataCollection
from state_estimator import StateEstimator
from goal_planning import GoalPlanning
from move_planning import MovePlanning
from control import Control
import config
import signal


class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm
    
class Commander:
    ARD = Arduino()
    DATA = DataCollection()
    STATE = StateEstimator()
    GOAL = GoalPlanning()
    MOVE = MovePlanning()
    CTRL = Control()

    def go(self):
        signal.signal(signal.SIGALRM, alarm_handler)
        if config.TIME_BEFORE_HALT > 0:
            signal.alarm(TIME_BEFORE_HALT)
        
        arduino.run()
        
        while True:
            DATA.run()
            STATE.run()
            GOAL.run()
            MOVE.run()
    
    def stop(self):
        DATA.stopVisionThread()
          
          
if __name__ == '__main__':
    try:
        cmdr = Commander()
        cmdr.go()
    except (KeyboardInterrupt, Alarm):
        cmdr.stop()
        sys.exit(0)
