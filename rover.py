from reflex import Reflex
from astarplanner import Planner
class Rover:

    def __init__(self, environment, battery, heuristic="manhattan"):
        self.env = environment
        self.curr_pos = self.env.start
        self.battery = battery
        self.reflex = Reflex(self.env)
        self.goal = self.reflex.set_goal(self.battery,self.curr_pos)

    def get_goal(self):
        return self.goal

        