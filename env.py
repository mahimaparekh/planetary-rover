import random

class Environment:
    terrain_cost = {
        'flat':5,
        'sandy':10,
        'sand-trap':15,
        'radiation':15,
        'rocky':1000
    }
    terrain_prob = {
        'flat':0.5,
        'sandy':0.2,
        'sand-trap':0.05,
        'radiation':0.05,
        'rocky':0.2
    }

    def __init__(self,size, stations, seed=None):
        if seed is not None:
            random.seed(seed)
        self.size = size
        self.num_stations = stations
        self.grid = self.set_grid()
        self.stations = set()
        self.start = (0,0)
        self.goal = (self.size-1, self.size-1)

        self.set_terrain()
        self.set_terrain_type(*self.start, 'flat')
        self.set_terrain_type(*self.goal, 'flat')
        self.set_recharge_stations()
    
    def set_grid(self):
        return [[None for col in range(self.size)] for row in range(self.size)]
    
    def set_terrain(self):
        terrains = list(self.terrain_prob.keys())
        probabilities = list(self.terrain_prob.values())

        for row in range(self.size):
            for col in range(self.size):
                self.grid[row][col]=random.choices(terrains,probabilities)[0]
    
    def display_grid(self):
        return self.grid
    
    def set_terrain_type(self,row,col,type):
        self.grid[row][col] = type
    
    def get_terrain(self,row,col):
        return self.grid[row][col]
    
    def is_hazardous(self,row,col):
        terrain_type = self.get_terrain(row,col)
        if(terrain_type=='sand-trap' or terrain_type=='radiation'):
            return True
        return False

    def get_terrain_cost(self,row,col):
        terrain_type = self.get_terrain(row,col)
        return self.terrain_cost[terrain_type]

    def get_neighbors(self, row, col):
        neighbors = []
        directions = [(-1, 0), 
                    (1, 0),   
                    (0, -1),  
                    (0, 1)]   

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                neighbors.append((new_row, new_col))
        return neighbors
    
    def set_recharge_stations(self):
        while len(self.stations) < self.num_stations:
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size - 1)

            if self.get_terrain(row,col)=='flat' and (row,col)!=self.start and (row,col)!=self.goal:
                self.stations.add((row,col))

    def get_stations(self):
        return self.stations
    
    def is_goal(self, row,col):
        if (row,col)==(self.size-1,self.size-1):
            return True
        return False
    
    def get_hazardous_zones(self):
        zones = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_hazardous(row,col):
                    zones.append((row,col))
        return zones







