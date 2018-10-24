import sys
import os
import arcade
from copy import deepcopy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

path = [
    [0, 0],
    [0, 10],
    [0, 20],
    [10, 20],
    [20, 20],
    [30, 20],
    [40, 20],
    [40, 30],
    [40, 40]
]

WIDTH = 100
HEIGHT = 100
MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * 6 + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * 6 + MARGIN

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.set_update_rate(1/2)
        self.path = path
        self.smooth_path = deepcopy(self.path)
        self.change = 1
        self.weight_data = 0.15
        self.weight_smooth = 0.1
        self.tolerance = 0.000001

    def draw_original_path(self):
        point_list = tuple(tuple([point[0]*5 + 200, point[1]*5 + 200]) for point in self.path)
        arcade.draw_line_strip(point_list, arcade.color.BLACK, 3)

    def draw_smooth_path(self):
        point_list = tuple(tuple([point[0]*5 + 200, point[1]*5 + 200]) for point in self.smooth_path)
        arcade.draw_line_strip(point_list, arcade.color.RED, 2)        

    def on_draw(self):
        arcade.start_render()
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
