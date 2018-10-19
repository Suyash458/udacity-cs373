grid = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0]
]

heuristic = [
    [9, 8, 7, 6, 5, 4],
    [8, 7, 6, 5, 4, 3],
    [7, 6, 5, 4, 3, 2],
    [6, 5, 4, 3, 2, 1],
    [5, 4, 3, 2, 1, 0]
]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [
    [-1, 0 ], # go up
    [ 0, -1], # go left
    [ 1, 0 ], # go down
    [ 0, 1 ] # go right
]

delta_name = ['^', '<', 'v', '>']
delta_name_dict = {
    '^': [-1, 0],
    '<': [0, -1],
    'v': [1, 0],
    '>': [0, 1]
}

min_func = 'f_val'

def get_init_state():
    return [{
        'f_val': heuristic[0][0],
        'g_val': 0,
        'pos': [0, 0],
        'path': ''
    }]

def get_all_moves(current_state, closed_states, grid):
    moves = []
    x, y = current_state
    closed_pos = [x['pos'] for x in closed_states]
    for move, name in zip(delta, delta_name):
        x_new = x + move[0]
        y_new = y + move[1]
        if len(grid) > x_new >= 0 and len(grid[0]) > y_new >= 0:
            if [x_new, y_new] not in closed_pos and not grid[x_new][y_new]:
                moves.append(([x_new, y_new], name))
    return moves

def get_min_state(open_states):
    open_states = sorted(open_states, key = lambda x: x[min_func])
    min_state = open_states[0] if open_states else []
    open_states = open_states[1::]
    return min_state, open_states

def check_goal(closed_states, goal):
    len([x for x in closed_states if x['pos'] == goal]) == 0

def get_final_state(closed_states, goal):
   return [x for x in closed_states if x['pos'] == goal][0]

def get_path(initial_grid, path, goal):
    grid_path = [[0 for col in row] for row in grid]
    x, y = (0, 0)
    for move_name in path:
        grid_path[x][y] = move_name
        move = delta_name_dict[move_name]
        x += move[0]
        y += move[1]
        grid_path[x][y] = move_name
    grid_path[goal[0]][goal[1]] = '*'
    return grid_path

def search(grid, init, goal, cost):
    expand = [[-1 for col in row] for row in grid]
    expand[0][0] = 0
    closed_states = [{
        'f_val': heuristic[0][0],
        'g_val': 0,
        'pos': [0, 0],
        'path': ''
    }]
    open_states = get_init_state()
    step = 0
    while not check_goal(closed_states, goal):
        if not open_states: return []
        min_state, open_states = get_min_state(open_states)
        expand[min_state['pos'][0]][min_state['pos'][1]] = step
        step += 1
        if min_state['pos'] == goal: break
        moves = get_all_moves(min_state['pos'], closed_states, grid)
        min_f = min_state['f_val']
        min_g = min_state['g_val']
        for move in moves:
            next_state = {
                'f_val': min_g + cost + heuristic[move[0][0]][move[0][1]],
                'g_val': min_g + cost,
                'pos': move[0],
                'path': min_state['path'] + move[1]
            }
            open_states.append(next_state)
            closed_states.append(next_state)
    final_state = get_final_state(closed_states, goal)
    path = get_path(grid, final_state['path'], goal)
    # print(final_state)
    # for row in path: print(row)
    # for row in expand: print(row)
    # print(expand)
    return final_state['path']

search(grid, init, goal, cost)
