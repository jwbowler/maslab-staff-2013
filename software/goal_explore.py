

class ExploreGoal:

    def __init__(self):
        self.sizeThreshFollow = 20 # min size of ball for switching from wall-follow to ball-follow
        self.sizeThreshSetGoal = 30 # min size of ball for transitioning to from this goal to the get-ball goal
        
    def getName(self):
        return "GOAL_EXPLORE"
        
    # Returns: (next_goal_name, action_name, action_arguments)
    def step(self, data):
        objTypes = [i[0] for i in data]
        
        # create filtered list of visible objects: remove non-balls and too small balls
        ball_list = [obj for obj in data
                     if ((obj[0] == "RED_BALL" or obj[0] == "GREEN_BALL")
                          and obj[2] >= self.sizeThreshFollow)]
                          
        if ball_list == []: # if no suitable balls:
            return (self.getName(), "ACTION_FOLLOW_WALL", data) # wall-follow
            
        ball_list.sort(key = lambda obj: obj[1][0]) # sort balls by distance
        target = (ball_list[0][1]) # target = (distance, angle) of best candidate ball
        
        if ball_list[0][2] > self.sizeThreshSetGoal: # if ball appears big enough:
            return ("GOAL_GET_BALL", "ACTION_HUNT_BALL", target) # commit to the "get-ball" goal
        else:
            return (self.getName(), "ACTION_HUNT_BALL", target) # else, stay in "exploring" mode but approach ball
            
