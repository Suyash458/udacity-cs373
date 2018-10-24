import sys
import os
import arcade
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimum_policy import grid, goal, cost, delta, get_init_value_grid, get_neighbors, get_min_cost

ROW_COUNT = len(grid)
COLUMN_COUNT = len(grid[0])

WIDTH = 100
HEIGHT = 100
MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

class MyGame(arcade.Window):
    def __init__(self, grid, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_update_rate(1/3)
        self.shape_list = None
        self.policy = get_init_value_grid(grid, goal, 99)
        self.current_cell = (goal[0], goal[1])
        self.changed = get_neighbors(grid, self.current_cell)
        self.recreate_grid()

    def overlay_cost(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * (ROW_COUNT - row - 1) + MARGIN + HEIGHT // 2
                text = f'{self.policy[row][column]:.2f}'
                color = arcade.color.BLACK if not grid[row][column] else arcade.color.WHITE
                arcade.draw_text(text, x, y, color)

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if (row, column) == self.current_cell:
                    color = arcade.color.GO_GREEN
                elif (row, column) in self.changed:
                    color = arcade.color.BABY_BLUE
                elif grid[row][column]:
                    color = arcade.color.SMOKY_BLACK
                else:
                    color = arcade.color.WHITE
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * (ROW_COUNT - row - 1) + MARGIN + HEIGHT // 2
                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

    def on_draw(self):
        arcade.start_render()
        self.shape_list.draw()
        self.overlay_cost()

    def on_update(self, delta_t):
        if not self.changed:
            return
        self.current_cell = self.changed.pop(last=False)
        stochastic_cost, optimal_direction = get_min_cost(grid, self.policy, self.current_cell)
        x, y = self.current_cell
        if stochastic_cost + cost < self.policy[x][y]:
            self.policy[x][y] = stochastic_cost + cost
            neighbors = get_neighbors(grid, self.current_cell)
            self.changed |= neighbors
        self.recreate_grid()
        self.overlay_cost()

def main():
    MyGame(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
