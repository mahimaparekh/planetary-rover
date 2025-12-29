class Planner:

    def __init__(self, environment, heuristic):
        self.env = environment
        self.heuristic = heuristic

    def get_path(self, curr_pos, goal,hazardous_cells):
        open_list = []
        closed_list = set()
        
        g_score = {}
        parent_tracker = {}

        g_score[curr_pos] = 0
        f_cost = self.calculate_heuristic(curr_pos, goal)

        open_list.append((f_cost, curr_pos))

        while open_list:
            open_list.sort(key=lambda x: x[0])
            f, node = open_list.pop(0)

            if node == goal:
                return self.reconstruct_path(parent_tracker, node)

            closed_list.add(node)

            for n in self.env.get_neighbors(node[0], node[1]):

                if n in closed_list:
                    continue
                if n in hazardous_cells:
                    continue
                if self.env.get_terrain(n[0],n[1])=='rocky':
                    continue

                g_cost = g_score[node] + self.env.get_terrain_cost(n[0], n[1])

                if n not in g_score or g_cost < g_score[n]:
                    parent_tracker[n] = node
                    g_score[n] = g_cost
                    f_cost = g_cost + self.calculate_heuristic(n, goal)

                    if n not in [node for _, node in open_list]:
                        open_list.append((f_cost, n))

        return None

    def reconstruct_path(self, parent_tracker, node):
        path = [node]
        while node in parent_tracker:
            node = parent_tracker[node]
            path.append(node)
        path.reverse()
        return path

    def calculate_heuristic(self, curr_pos, goal):
        if self.heuristic == 'manhattan':
            return abs(curr_pos[0] - goal[0]) + abs(curr_pos[1] - goal[1])
