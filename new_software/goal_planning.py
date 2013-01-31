import commander as c
from config import *
import time

class GoalPlanning:

    # List of goals
    HUNT = 0
    BUTTON = 1
    SCORE = 2
    goalNames = ["HUNT","BUTTON", "SCORE"]

    #list of target types
    BALL = 0
    BUTTON = 1
    TOWER = 2
    targetNames = ["BALL", "BUTTON", "TOWER"]
    
    
    def __init__(self):
        self.goal = GoalPlanning.HUNT
        #self.goal = GoalPlanning.SCORE
        self.target = None
        self.targetType = None 
    
    # Updates current goal according to estimated state
    def run(self):
        self.chooseGoal()
        self.chooseTarget()

    def chooseGoal(self):
        if 0 < c.STATE().getTimeRemaining() < ONLY_SCORE_PERIOD:
            self.goal = self.SCORE
        else:
            self.goal = self.HUNT

    def chooseTarget(self):
        self.target = None

        if self.getGoal() == self.HUNT:
            self.target = c.STATE().getNearestBall()
            self.targetType = self.BALL
        elif self.getGoal() == self.BUTTON:
            self.target = c.STATE().getButton()
            self.targetType = self.BUTTON
        elif self.getGoal() == self.SCORE:
            #self.target = c.STATE().getTowerMiddle()
            self.target = c.STATE().getTowerBase()
            self.targetType = self.TOWER

        if self.target == None:
            self.targetType = None


    def log(self):
        c.LOG("~~~GOAL~~~")
        c.LOG("Goal: " + self.goalNames[self.getGoal()])
        
    # Returns current goal
    def getGoal(self):
        return self.goal

    def getTarget(self):
        return self.target

    def getTargetType(self):
        return self.targetType

        
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
