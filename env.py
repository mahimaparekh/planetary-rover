import random

class Environment:
    # dictionary for the cost of terrains
    terrain_cost = {
        'flat':5,
        'sandy':10,
        'sand-trap':15,
        'radiation':15,
        'rocky':1000
    }
    # pribability of each terrain
    terrain_prob = {
        'flat':0.5,
        'sandy':0.2,
        'sand-trap':0.05,
        'radiation':0.05,
        'rocky':0.2
    }

    # constructor
    def __init__(self,height,width, seed=None):
        if seed is not None:
            random.seed(seed)
        self.width = width
        self.height = height
        self.grid = self.set_grid()
    
    # initializing the grid
    def set_grid(self):
        return [[None for col in range(self.width)] for row in range(self.height)]
    
    # setting the terrains on the grid
    def set_terrain(self):
        terrains = list(self.terrain_prob.keys())
        probabilities = list(self.terrain_prob.values())

        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col]=random.choices(terrains,probabilities)[0]
    
    # returns the grid
    def display_grid(self):
        return self.grid
    
    # returns the terrain type
    def get_terrain(self,row,col):
        return self.grid[row][col]
    
    # checks if terrain is hazardous (sand-trap or radiation-hotspot)
    def is_hazardous(self,row,col):
        terrain_type = self.get_terrain(row,col)
        if(terrain_type=='sand-trap' or terrain_type=='radiation'):
            return True
        return False

    # returns terrain cost
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

            # checks if co-ordinates are within bounds
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                neighbors.append((new_row, new_col))

        return neighbors





