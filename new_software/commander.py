ard = Arduino()
data = DataCollection(ard)
state = StateEstimator(data)
goal = GoalPlanning(state)
move = MovementPlanning(state, goal, ctrl)
ctrl = Control(ard)

while True:
    data.run()
    state.run()
    goal.run()
    move.run()
