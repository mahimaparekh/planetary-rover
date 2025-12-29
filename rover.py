from reflex import Reflex
from astarplanner import Planner

class Rover:

    def __init__(self, environment, battery, heuristic="manhattan"):
        self.env = environment
        self.curr_pos = self.env.start
        self.battery = battery
        self.final_goal = self.env.goal
        self.heuristic = heuristic

        self.hazardous_cells = set()
        self.reflex = Reflex(self.env)
        self.safe_cell = self.curr_pos

        self.iteration = 1


    def run(self):
        print("Recharge stations locations: ")
        print(self.env.get_stations())
        print("Start location: ",self.env.start)
        while self.curr_pos != self.final_goal:
            self.goal = self.reflex.set_goal(self.battery, self.curr_pos)
            if self.goal == 'Dead':
                print("Battery depleted. Rover did not reach goal!")
                return False
            
            if self.goal == self.final_goal:
                print("Final Goal:", self.final_goal)
            elif self.goal != self.final_goal:
                print("Battery low. Goal set to charging station at:", self.goal)

            if self.curr_pos == self.goal:
                if self.goal == self.final_goal:
                    print("Final goal reached:", self.final_goal)
                    break
                else:
                    print("Reached recharge station:", self.goal)
                    self.battery = 100
                    print("Battery recharged to 100%")
                    continue

            print("\nIteration:", self.iteration)
            self.iteration += 1
            print("Current position:", self.curr_pos)
            print("Current goal:", self.goal)
            print("Battery level:", self.battery)

            planner = Planner(self.env, self.heuristic)
            path = planner.get_path(self.curr_pos, self.goal, self.hazardous_cells)

            if path is None:
                print("No path found. Mission failed.")
                return False

            print("Path received:", path)

            success = self.follow_path(path)

            if success == 'Dead':
                print("Battery depleted during path following! Rover did not reach goal.")
                return False
            
            if not success:
                print("Replanning due to hazard or battery condition.")

        print("🎯 Final goal reached:", self.final_goal)
        return True

    def follow_path(self, path):
        for cell in path[1:]:  # skip current position
            move_cost = self.env.get_terrain_cost(cell[0], cell[1])
            if self.battery < move_cost:
                return 'Dead'

            self.move_rover(cell)
            
            self.battery -= move_cost
            print(f"Moved to {cell} | Battery: {self.battery} (cost: {move_cost})")

            if cell in self.env.get_stations():
                print("Rover at recharge station. Recharging to 100%!")
                self.battery = 100

            if self.battery <= 0:
                print(f"Battery depleted at {cell}")
                return 'Dead'

            if self.env.is_hazardous(cell[0], cell[1]):
                print("Hazard encountered at", cell)
                self.hazardous_cells.add(cell)
                backtrack_cost = self.env.get_terrain_cost(self.safe_cell[0], self.safe_cell[1])
                if self.battery < backtrack_cost:
                    print(f"Insufficient battery to backtrack. Battery dead.")
                    return 'Dead'
                self.move_rover(self.safe_cell)
                self.battery -= backtrack_cost
                print(f"Backtracked to {self.safe_cell} | Battery: {self.battery}")
                return False  

            self.safe_cell = cell

            new_goal = self.reflex.set_goal(self.battery, self.curr_pos)

            if new_goal == 'Dead':
                return 'Dead'

            if new_goal != self.goal and new_goal != self.final_goal:
                print(f"Goal changed from {self.goal} to {new_goal}")
                self.goal = new_goal
                return False

        return True

    def move_rover(self, cell):
        self.curr_pos = cell