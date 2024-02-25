# adapted from https://github.com/slavadev/snake_nn/blob/master/snake_game.py

import curses
import json
from random import randint
import csv
import numpy as np


class SnakeGame:
    def __init__(self, board_width=20, board_height=20, gui=False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        self.direction = -1

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

        if abs(self.direction - key) == 2:
            key = self.direction

        self.direction = key

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
        arr_tuples = [tuple(x) for x in self.snake]
        has_duplicates = len(arr_tuples) != len(set(arr_tuples))

        if (has_duplicates or self.snake[0][0] == 0 or  # head of snake is 0
                self.snake[0][0] == self.board["width"] + 1 or  # head of snake crosses outside borders
                self.snake[0][1] == 0 or self.snake[0][1] == self.board["height"] + 1 or self.snake[0] in self.snake[
                                                                                                          1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def get_cell_value_safe(self, x, y):
        try:
            value = self.board_matrix[x][y]
            return value
        except IndexError:
            return 1.0

    def generate_vision_array(self):
        """
        Generate a len(4) binary array representing whether the cells immediately surrounding the head of the snake
        are filled or unfilled.

        The array is in format [N,E,S,W] from the snakes POV.

        # TODO: decide wether or not to normalize these directions over all snake directions.
        Right now they are normalized but they might not need to be because directions are absolute.
        """

        headX, headY = self.snake[0]

        if self.direction < 0: return [None, None, None, None]

        north_cell = self.get_cell_value_safe(headX - 1, headY)
        south_cell = self.get_cell_value_safe(headX + 1, headY)
        west_cell = self.get_cell_value_safe(headX, headY - 1)
        east_cell = self.get_cell_value_safe(headX, headY + 1)

        # from snake Head POV, format of the array is [N,E,S,W]
        if self.direction == 0: return [north_cell, east_cell, south_cell, west_cell]
        if self.direction == 1: return [east_cell, south_cell, west_cell, north_cell]
        if self.direction == 2: return [south_cell, west_cell, north_cell, east_cell]
        if self.direction == 3: return [west_cell, north_cell, east_cell, south_cell]

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: self.render_destroy()
        raise Exception("Game over")



if __name__ == "__main__":
    # options:
    SHOW_GUI = True
    BOARD_HEIGHT = 10
    BOARD_WIDTH = 10
    NUM_GAMES = 2
    SAVE_MATRIX = True

    # clear output files
    with open('output.csv', 'w') as file:
        pass

    with open('matrix_output.txt', 'w') as file:
        pass

    # write header line to output csv
    with open('output.csv', mode='a', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write headers
        writer.writerow(
            ['n', 'gameOver', 'food', 'score', 'snakeHead', 'snakeCells', 'visionN', 'visionE', 'visionS', 'visionW',
             'directionChoice', 'directionCurrent'])

    for _ in range(NUM_GAMES):
        # initiate new game
        game = SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
        game.start()

        n = 0
        gameOver = False
        gameHistory = []
        snakeHistory = {}

        while not gameOver:
            directionChoice = randint(0, 3)

            done, score, snake, food = game.generate_observations()

            [visionN, visionE, visionS, visionW] = game.generate_vision_array()

            data = [n, done, game.food, score, snake[0], snake, visionN, visionE, visionS, visionW, directionChoice,
                    game.direction]

            snakeHistory[str(n)] = snake

            if SAVE_MATRIX:
                # Write matrix to file
                with open('matrix_output.txt', 'a') as file:
                    file.write(str("------- MOVE " + str(n) + " ------- \n"))
                    np.savetxt(file, game.board_matrix, fmt='%d', delimiter=' ', newline="\n")

            # iterate game by one step
            try:
                game.step(directionChoice)
            except:
                gameOver = True

            n += 1

            with open('output.csv', mode='a', newline='') as file:
                # Create a CSV writer object
                writer = csv.writer(file)
                # Write headers
                writer.writerow(data)