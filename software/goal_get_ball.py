

class GetBallGoal:
    
    def __init__(self):
        self.sizeThresh = 25
        self.distanceThresh = 0.1
        self.bCapturingBall = False
        self.captureIterationCounter = 30
        
    def getName(self):
        return "GOAL_GET_BALL"
        
    # Returns: (next_goal_name, action_name, action_arguments)
    def step(self, data):
    
        if self.bCapturingBall == True: # if we're midway through a capture sequence:
            if self.captureIterationCounter <= 0: # if we've run it for enough iterations:
                self.bCapturingBall = False # don't continue after this
                self.captureIterationCounter = 30
                return (self.getName(), "ACTION_CAPTURE_BALL", False) # run with "false" argument to shut off ball collector motor
            else:
                self.captureIterationCounter -= 1
                return (self.getName(), "ACTION_CAPTURE_BALL", True) # continue         
    
        # create filtered list of visible objects: remove non-balls and too small balls
        ball_list = [obj for obj in data
                     if ((obj[0] == "RED_BALL" or obj[0] == "GREEN_BALL")
                          and obj[2] >= self.sizeThresh)]
                          
        if ball_list == []: # if all balls have somehow disappeared:
            return ("GOAL_EXPLORE", "ACTION_FOLLOW_WALL", data) # switch back to "explore" goal
            
        ball_list.sort(key = lambda obj: obj[1][0]) # sort balls by distance
        target = (ball_list[0][1]) # target = (distance, angle) of best candidate ball
        
        if target[0] < self.distanceThresh: # if calculated distance is enough:
            # capture dat shit
            self.bCapturingBall = True;
            self.captureIterationCounter -= 1
            return (self.getName(), "ACTION_CAPTURE_BALL", True)
        else:
            return (self.getName(), "ACTION_HUNT_BALL", target) # else, keep driving towards it
        
