class Commander:
    ARD = Arduino()
    DATA = DataCollection()
    STATE = StateEstimator()
    GOAL = GoalPlanning()
    MOVE = MovementPlanning()
    CTRL = Control()

    def go(self):
      while True:
          DATA.run()
          STATE.run()
          GOAL.run()
          MOVE.run()
