import commander as c
from config import *
import time

class GoalPlanning:

    # List of goals
    HUNT = 0
    HUNT_AND_SCORE = 1
    goalNames = ["HUNT", "HUNT_AND_SCORE"]
    
    def __init__(self):
        self.goal = GoalPlanning.HUNT
    
    # Updates current goal according to estimated state
    def run(self):
        if c.STATE().getTimeRemaining() < ONLY_SCORE_PERIOD:
            #self.goal = GoalPlanning.SCORE_AND_LOITER
            pass
        elif c.STATE().getTimeSinceLastScore() < MIN_WAIT_BETWEEN_SCORING:
            self.goal = GoalPlanning.HUNT
        else:
            self.goal = GoalPlanning.HUNT_AND_SCORE

    def log(self):
        c.LOG("~~~GOAL~~~")
        c.LOG("Goal: " + self.goalNames[self.getGoal()])
        
    # Returns current goal
    def getGoal(self):
        return self.goal
        
if __name__ == "__main__":
    c.ARD()
    c.DATA()
    c.STATE()
    c.GOAL()
    c.ARD().run()

    while True:
        c.DATA().run()

        c.STATE().run()
        c.STATE().log()

        c.GOAL().run()
        c.GOAL().log()
        time.sleep(.5)
