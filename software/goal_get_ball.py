import time

class GetBallGoal:
    
    def __init__(self):
        self.distThreshMin = 2
        self.distanceThresh = 0.25

        self.capturingBall = False
        self.captureIterationCounter = 30
        self.captureEndTime = 0
        self.captureTime = 2 #in seconds
        
    def getName(self):
        return "GOAL_GET_BALL"
        
    # Returns: (next_goal_name, action_name, action_arguments)
    def step(self, data):
        ir = [obj[1] for obj in data if (obj[0] == "IR")]
        for meas in ir:
            if meas[0] < 600:
                return (self.getName(), "ACTION_EMERGENCY_REVERSE", None)
    
        if self.capturingBall == True:
            if time.time() > self.captureEndTime:
                self.capturingBall = False
                return (self.getName(), "ACTION_CAPTURE_BALL", False) # run with "false" argument to shut off ball collector motor

            return (self.getName(), "ACTION_CAPTURE_BALL", True) # continue         
    
        # create filtered list of visible objects: remove non-balls and too small balls
        ball_list = [obj for obj in data
                     if ((obj[0] == "RED_BALL" or obj[0] == "GREEN_BALL")
                          and obj[2] >= self.distThreshMin)]
                          
        if ball_list == []: # if all balls have somehow disappeared:
            return ("GOAL_EXPLORE", "ACTION_ROTATE_IN_PLACE", data)
            
        ball_list.sort(key = lambda obj: obj[1][0]) # sort balls by distance
        target = (ball_list[0][1]) # target = (distance, angle) of best candidate ball
        
        if target[0] < self.distanceThresh: #if calculated distance is enough:
            # capture dat shit
            self.capturingBall = True;
            self.captureEndTime = time.time() + self.captureTime
            return (self.getName(), "ACTION_CAPTURE_BALL", True)
        else:
            return (self.getName(), "ACTION_HUNT_BALL", target) # else, keep driving towards it
        
