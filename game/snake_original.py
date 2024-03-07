# adapted from https://github.com/slavadev/snake_nn/blob/master/snake_game.py
# contains all game logic and methods to export game state from an active game

import curses
from random import randint
import numpy as np


class SnakeGame:
    def __init__(self, board_width=20, board_height=20, gui=False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

        # matrix representation of the whole board
        self.board_matrix = np.zeros((self.board['width'], self.board['height']))

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0, 1) == 0
        self.direction = 2 if vertical else 1
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

            # update snake location in matrix
            self.board_matrix[point[0], point[1]] = 1

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food  # TODO: update food location in matrix

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(200)
        self.win = win
        self.render()

    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addch(self.food[0], self.food[1], '🍎')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], '🔸')
            else:
                self.win.addch(point[0], point[1], '🔹')
        self.win.getch()

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT

        # prevent snake from running back on itself: if an input direction is
        # the exact opposite of current direction, do not change direction.
        # This reflects original game behaviours.-Henry

        if self.done == True: self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions()
        if self.gui: self.render()
        return self.generate_observations()

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
        elif key == 1:
            new_point[1] += 1
        elif key == 2:
            new_point[0] += 1
        elif key == 3:
            new_point[1] -= 1
        self.snake.insert(0, new_point)
        self.board_matrix[new_point[0], new_point[1]] = 1

    def remove_last_point(self):
        last_point = self.snake.pop()
        self.board_matrix[last_point[0], last_point[1]] = 0

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):

        # Check for duplicates - representing whether the snake has run into itself or not.
        # This makes the snake die- same as original game.

        if (    self.snake[0][0] == 0 or  # head of snake is 0
                self.snake[0][0] == self.board["width"] + 1 or  # head of snake crosses outside borders
                self.snake[0][1] == 0 or
                self.snake[0][1] == self.board["height"] + 1 or
                self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def get_cell_value_safe(self, x, y):
        if x < 0 or x > self.board['height'] - 1 or y < 0 or y > self.board['width'] - 1:
            return 1.0
        return self.board_matrix[x][y]

    def generate_vision_array(self):
        """
        Generate a len(4) binary array representing whether the cells immediately surrounding the head of the snake
        are filled or unfilled.
        """

        headX, headY = self.snake[0]

        # make sure direction is actully deinfed
        if self.direction < 0: return [None, None, None, None]

        up_cell = self.get_cell_value_safe(headX - 1, headY)
        down_cell = self.get_cell_value_safe(headX + 1, headY)
        left_cell = self.get_cell_value_safe(headX, headY - 1)
        right_cell = self.get_cell_value_safe(headX, headY + 1)

        return [up_cell, right_cell, down_cell, left_cell]

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: self.render_destroy()
        raise Exception("Game over")
