import sys
import os
import arcade
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from a_star import grid, heuristic, init, goal, cost, search

ROW_COUNT = len(grid)
COLUMN_COUNT = len(grid[0])

WIDTH = 90
HEIGHT = 90
MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
TURTLE_HEIGHT = 20
TURTLE_BASE = 20

def get_grid_points(row, column):
    x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
    y = (MARGIN + HEIGHT) * (ROW_COUNT - row - 1) + MARGIN + HEIGHT // 2
    return [x, y]

class MyGame(arcade.Window):
    def __init__(self, grid, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_update_rate(1/2)
        self.shape_list = None
        self.grid = grid
        self.turtle_center = [
            MARGIN + WIDTH // 2,
            (MARGIN + HEIGHT) * (ROW_COUNT - 1) + MARGIN + HEIGHT // 2
        ]
        self.turtle = self.create_turtle(self.turtle_center[0], self.turtle_center[1])
        self.path = search(grid, heuristic, init, goal, cost)
        self.visited = []
        self.recreate_grid()

    def create_turtle(self, center_x, center_y, base=30, height=25):
        point_list = [
            (center_x - base//2, center_y + height//2),
            (center_x + base//2, center_y + height//2),
            (center_x, center_y - (height//2 + 5)),
        ]
        color_list = [
            arcade.color.BLACK,
            arcade.color.BLACK,
            arcade.color.BLACK
        ]
        return arcade.create_triangles_filled_with_colors(point_list, color_list)

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 0:
                    if [row, column] not in self.visited:
                        color = arcade.color.BABY_BLUE
                    else:
                        color = arcade.color.WHITE
                else:
                    color = arcade.color.BLACK
                x, y = get_grid_points(row, column)
                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)
        self.shape_list.append(self.turtle)

    def on_update(self, delta_t):
        try:
            pos = next(self.path)['pos']
            self.turtle_center = get_grid_points(pos[0], pos[1])
            self.turtle = self.create_turtle(self.turtle_center[0], self.turtle_center[1])
        except:
            pass
        self.recreate_grid()
        self.shape_list.draw()
        self.visited.append(pos)

    def on_draw(self):
        arcade.start_render()
        self.shape_list.draw()

def main():
    MyGame(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()