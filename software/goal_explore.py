class ExploreGoal:

    def __init__(self):
        self.distThreshFollow = 5 # min size of ball for switching from wall-follow to ball-follow
        self.distThreshSetGoal = 1 # min size of ball for transitioning to from this goal to the get-ball goal
        
    def getName(self):
        return "GOAL_EXPLORE"

    # Returns: (next_goal_name, action_name, action_arguments)
    def step(self, data):
        ball_list = [obj for obj in data
                     if ((obj[0] == "RED_BALL" or obj[0] == "GREEN_BALL"))]

        ir = [obj[1] for obj in data if (obj[0] == "IR")]
        for meas in ir:
            if meas[0] > 400:
                return (self.getName(), "ACTION_EMERGENCY_REVERSE", None)
                          
        if ball_list == []: # if no suitable balls:
            return (self.getName(), "ACTION_ROTATE_IN_PLACE", 1)
            
        ball_list.sort(key = lambda obj: obj[1][0]) # sort balls by distance
        target = (ball_list[0][1]) # target = (distance, angle) of best candidate ball
        
        
        if target[0] < self.distThreshSetGoal: # if ball appears big enough:
            return ("GOAL_GET_BALL", "ACTION_ROTATE_IN_PLACE", -1)
        else:
            return (self.getName(), "ACTION_HUNT_BALL", target)
