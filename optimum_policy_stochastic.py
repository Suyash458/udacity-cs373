from utils import OrderedSet

grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

goal = [0, len(grid[0])-1]
cost = 1

delta = [
    [-1, 0 ],
    [ 0, -1],
    [ 1, 0 ],
    [ 0, 1 ]
]

delta_name = ['^', '<', 'v', '>']

MAX_COST = 1000

def get_init_value_grid(grid, goal, max_cost):
    policy = [[max_cost for _ in range(len(grid[0]))] for _ in range(len(grid))]
    policy[goal[0]][goal[1]] = 0
    return policy

def get_init_policy(grid, goal):
    policy = [[' ' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    policy[goal[0]][goal[1]] = '*'
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

def calculate_stochastic_cost(current_cell, adj, value):
    x, y = current_cell
    x_adj, y_adj = adj
    success_prob = 0.5
    failure_prob = (1.0 - success_prob)/2.0
    collision_cost = MAX_COST
    if x != x_adj:
        left_cost = failure_prob * (value[x][y - 1] if len(grid[0]) > y - 1 >= 0 else collision_cost)
        right_cost = failure_prob * (value[x][y + 1] if len(grid[0]) > y + 1 >= 0 else collision_cost)
        return (success_prob * value[x_adj][y_adj]) + left_cost + right_cost
    else:
        top_cost = failure_prob * (value[x - 1][y] if len(grid) > x - 1 >= 0 else collision_cost)
        bottom_cost = failure_prob * (value[x + 1][y] if len(grid) > x + 1 >= 0 else collision_cost)
        return (success_prob * value[x_adj][y_adj]) + top_cost + bottom_cost

def get_min_cost(grid, value, current_cell):
    x, y = current_cell
    if grid[x][y]:
        return MAX_COST
    return min([calculate_stochastic_cost(current_cell, adj, value) for adj in get_neighbors(grid, current_cell)])

def get_optimal_direction(grid, value, current_cell):
    x, y = current_cell
    if grid[x][y]:
        return ' '
    neighbors = get_neighbors(grid, current_cell)
    min_adj = None
    min_value = MAX_COST
    for adj in neighbors:
        stochastic_cost = calculate_stochastic_cost(current_cell, adj, value)
        if min_value > stochastic_cost:
            min_value = stochastic_cost
            min_adj = adj
    if x - min_adj[0] == 1 and y - min_adj[1] == 0: return '^'
    if x - min_adj[0] == -1 and y - min_adj[1] == 0: return 'v'
    if x - min_adj[0] == 0 and y - min_adj[1] == 1: return '<'
    if x - min_adj[0] == 0 and y - min_adj[1] == -1: return '>'

def compute_value(grid, goal, cost):
    value = get_init_value_grid(grid, goal, MAX_COST)
    policy = get_init_policy(grid, goal)
    change = OrderedSet()
    change |= (get_neighbors(grid, goal))
    while change:
        current_cell = change.pop(last=False)
        stochastic_cost = get_min_cost(grid, value, current_cell)
        min_direction = get_optimal_direction(grid, value, current_cell)
        if stochastic_cost + cost < value[current_cell[0]][current_cell[1]]:
            value[current_cell[0]][current_cell[1]] = stochastic_cost + cost
            policy[current_cell[0]][current_cell[1]] = min_direction
            neighbors = get_neighbors(grid, current_cell)
            change |= (neighbors)
    for row in policy: print(row)
    for row in value: print(row)
    return value

compute_value(grid, goal, cost)