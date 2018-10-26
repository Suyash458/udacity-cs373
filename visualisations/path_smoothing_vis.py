import sys
import os
import arcade
from copy import deepcopy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from a_star import search

grid = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
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

ROW_COUNT = len(grid)
COLUMN_COUNT = len(grid[0])

WIDTH = 100
HEIGHT = 100
MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

def get_grid_path(path):
    return [get_grid_points(p[0], p[1]) for p in path]

def get_grid_points(row, column):
    x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
    y = (MARGIN + HEIGHT) * (ROW_COUNT - row - 1) + MARGIN + HEIGHT // 2
    return [x, y]

def lerp(v0, v1, i):
    return v0 + i * (v1 - v0)

def get_equidistant_points(p1, p2, n):
    return [[lerp(p1[0],p2[0],1./n*i), lerp(p1[1],p2[1],1./n*i)] for i in range(n+1)]

def get_extended_path(path):
    new_path = []
    for i in range(len(path) - 1):
        new_path += get_equidistant_points(path[i], path[i+1], 15)
    return new_path


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_update_rate(1/10)
        self.shape_list = None   
        *_, self.final_state = search(grid, heuristic, init, goal, cost)
        self.path = get_extended_path(get_grid_path(self.final_state['path']))
        self.smooth_path = deepcopy(self.path)
        self.change = 1
        self.weight_data = 0.02
        self.weight_smooth = 0.4
        self.tolerance = 0.000001

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if grid[row][column]:
                    color = arcade.color.SMOKY_BLACK
                else:
                    color = arcade.color.WHITE
                x, y = get_grid_points(row, column)
                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

    def draw_original_path(self):
        point_list = tuple(tuple([point[0], point[1]]) for point in self.path)
        arcade.draw_line_strip(point_list, arcade.color.BLACK, 5)

    def draw_smooth_path(self):
        point_list = tuple(tuple([point[0], point[1]]) for point in self.smooth_path)
        arcade.draw_line_strip(point_list, arcade.color.RED, 5)        

    def on_draw(self):
        arcade.start_render()
        self.recreate_grid()
        self.shape_list.draw()
        self.draw_original_path()
        self.draw_smooth_path()

    def on_update(self, delta_t):
        if self.change >= self.tolerance:
            self.change = 0.0
            for i in range(1, len(self.path) - 1):
                for j in range(2):
                    old = self.smooth_path[i][j]
                    self.smooth_path[i][j] += self.weight_data * (self.path[i][j] - self.smooth_path[i][j]) + self.weight_smooth * (self.smooth_path[i-1][j] + self.smooth_path[i+1][j] - 2.0 * self.smooth_path[i][j]) 
                    self.change += abs(old - self.smooth_path[i][j])
        self.draw_smooth_path()

def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
