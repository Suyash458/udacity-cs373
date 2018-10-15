from utils import OrderedSet

grid = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0]
]

goal = [len(grid)-1, len(grid[0])-1]
cost = 1 

delta = [
    [-1, 0 ],
    [ 0, -1], 
    [ 1, 0 ], 
    [ 0, 1 ]
]

delta_name = ['^', '<', 'v', '>']

def get_init_policy(grid, goal, max_cost):
    policy = [[max_cost for _ in range(len(grid[0]))] for _ in range(len(grid))]
    policy[goal[0]][goal[1]] = 0    
    return policy

def get_neighbors(grid, current_cell):
    neighbors = OrderedSet()
    x, y = current_cell
    for move in delta:
        x_new = x + move[0]
        y_new = y + move[1]
        if len(grid) > x_new >= 0 and len(grid[0]) > y_new >= 0:
            if not grid[x_new][y_new]:
                neighbors.add((x_new, y_new))
    return neighbors

def get_min_cost(grid, policy, current_cell):
    x, y = current_cell
    if grid[x][y]:
        return MAX_COST
    return min([policy[adj[0]][adj[1]] for adj in get_neighbors(grid, current_cell)])

def compute_value(grid, goal, cost):
    policy = get_init_policy(grid, goal, 99)
    change = OrderedSet()
    change |= (get_neighbors(grid, goal))
    while change:
        current_cell = change.pop(last=False)
        current_cost = get_min_cost(grid, policy, current_cell)
        if current_cost + cost < policy[current_cell[0]][current_cell[1]]:
            policy[current_cell[0]][current_cell[1]] = current_cost + cost
            neighbors = get_neighbors(grid, current_cell)
            change |= (neighbors)
    return policy