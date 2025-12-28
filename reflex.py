import math
class Reflex:

    def __init__(self, environment):
        self.env = environment
    
    def set_goal(self, battery, curr_pos):
        if(battery<=20):
            return self.find_nearest_station(curr_pos)
        elif(battery>20 and battery<=25):
            station = self.find_nearest_station(curr_pos)
            if math.dist(curr_pos,station)<=2:
                return station
            else:
                return self.env.goal
        else:
            return self.env.goal
        
    def find_nearest_station(self,curr_pos):
        stations = self.env.stations
        nearest = None
        min_dist = float('inf')
        for s in stations:
            distance = math.dist(s,curr_pos)
            if(distance<min_dist):
                min_dist = distance
                nearest = s
        return nearest