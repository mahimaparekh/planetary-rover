import math
from env import Environment
from rover import Rover

env = Environment(size=30, stations=30, seed=42)
rover = Rover(environment=env, battery=100, heuristic='manhattan')
rover.run()
