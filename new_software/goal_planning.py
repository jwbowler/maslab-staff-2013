import commander as c
import time

class GoalPlanning:

    # List of goals
    FIND_BALLS = 0
    SCORE_TOWER = 1
    PRESS_BUTTON = 2
    SCORE_WALL = 3
    WAIT_AT_WALL = 4
    goalNames = ["FIND_BALLS", "SCORE_TOWER", "PRESS_BUTTON", "SCORE_WALL", "WAIT_AT_WALL"]
    
    def __init__(self):
        self.goal = GoalPlanning.FIND_BALLS
        self.target = None
    
    # Updates current goal according to estimated state
    def run(self):
        if self.goal == GoalPlanning.FIND_BALLS:
            self.target = c.STATE().getMyNearestBall()

    def log(self):
        print "~~~GOAL~~~"
        print "Goal: " + self.goalNames[self.getGoal()]
        print "Target: " + str(self.getTarget())
        print "~~~GOAL~~~"
        
    # Returns current goal
    def getGoal(self):
        return self.goal
        
    # Returns (distance, angle) if applicable to goal, or None if not applicable
    def getTarget(self):
        return self.target

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
