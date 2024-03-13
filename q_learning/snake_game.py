import curses
from random import randint
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
        return self.generate_observations(reward = 0)

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        self.snake_dict = {} # used for vision array
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
        self.food = food  

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
        reward = 0
        if self.done == True: 
            reward = -10
            self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
            reward = 10
        else:
            self.remove_last_point()
            reward = self.check_collisions()
        if self.gui: self.render()
        return self.generate_observations(reward)

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
        if new_point[0] == 20 or new_point[1] == 20:
            self.end_game()
        else:
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
                self.snake[0][0] == self.board["width"] or  # head of snake crosses outside borders
                self.snake[0][1] == 0 or self.snake[0][1] == self.board["height"] or self.snake[0] in self.snake[
                                                                                                          1:-1]):
            self.done = True
            return -10
        return 0

    def generate_observations(self, reward = 0):
        # return self.done, self.score, self.snake, self.food
        danger_array = self.generate_vision_array()
        direction_array = [int(self.direction == 0), int(self.direction == 1), int(self.direction == 2), int(self.direction == 3)]
        food_location_array, distance_to_food = self.get_food_location()
        return np.concatenate((danger_array, direction_array, food_location_array)), reward, self.done, self.score, distance_to_food

    def run_into_wall(self, x, y):
        if x < 0 or x > self.board['height'] - 1 or y < 0 or y > self.board['width'] - 1:
            return 0
        return 1

    def generate_vision_array(self):
        """
        Generate a len(4) binary array representing whether the cells immediately surrounding the head of the snake
        are filled or unfilled.
        """

        headX = self.snake[0][0]
        headY = self.snake[0][1]

        # make sure direction is actully deinfed
        if self.direction < 0: return [None, None, None, None]

        up_cell = int((self.run_into_wall(headX - 1, headY)) and ([headX - 1, headY] in self.snake))
        down_cell = int((self.run_into_wall(headX + 1, headY)) and ([headX + 1, headY] in self.snake))
        left_cell = int((self.run_into_wall(headX, headY - 1)) and ([headX, headY - 1] in self.snake))
        right_cell = int((self.run_into_wall(headX, headY + 1)) and ([headX, headY + 1] in self.snake))

        if self.direction == 0:
            return [up_cell, left_cell, right_cell]
        elif self.direction == 1:
            return [right_cell, up_cell, down_cell]
        elif self.direction == 2:
            return [down_cell, right_cell, left_cell]
        else:
            return [left_cell, down_cell, up_cell]

    def get_food_location(self):
        headX, headY = self.snake[0]
        foodX, foodY = self.food[0], self.food[1]
        food_locations = [int(headY < foodY), int(headX < foodX), int(headY > foodY), int(headX > foodX)]
        distance_to_food = [abs(headX - foodX), abs(headY - foodY)]
        return food_locations, distance_to_food

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: self.render_destroy()
        self.done = True
        


# if __name__ == "__main__":
#     # options:
#     SHOW_GUI = False
#     BOARD_HEIGHT = 10
#     BOARD_WIDTH = 10
#     NUM_GAMES = 1
#     SAVE_MATRIX = True
#
#     # clear output files
#     with open('../data_collection/output.csv', 'w') as file:
#         pass
#
#     with open('../data_collection/matrix_output.txt', 'w') as file:
#         pass
#
#     # write header line to output csv
#     with open('../data_collection/output.csv', mode='a', newline='') as file:
#         # Create a CSV writer object
#         writer = csv.writer(file)
#         # Write headers
#         writer.writerow(
#             ['n', 'gameOver', 'head', 'score', 'visionUp', 'visionRight', 'visionDown', 'visionLeft',
#              'directionChoice'])
#
#     for _ in range(NUM_GAMES):
#         n = 0
#         gameOver = False
#         gameHistory = []
#
#         # initiate a new game
#         game = SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
#         game.start()
#
#         directionChoice = randint(0, 3)
#
#         while not gameOver:
#             # get game state info
#             done, score, snake, food = game.generate_observations()
#             [visionUp, visionRight, visionDown, visionLeft] = game.generate_vision_array()
#             data = [n, gameOver, game.snake[0], score, visionUp, visionRight, visionDown, visionLeft, directionChoice]
#
#             if SAVE_MATRIX:
#                 # Write matrix to file
#                 with open('../data_collection/matrix_output.txt', 'a') as file:
#                     file.write(str("------- MOVE " + str(n) + " ------- \n"))
#                     np.savetxt(file, game.board_matrix, fmt='%d', delimiter=' ', newline="\n")
#
#             # iterate game by one step
#             try:
#                 # SNAKE LIVES:
#                 game.step(directionChoice)
#                 data[1] = 0 # this sets the gameOver variable to false
#                 gameHistory.append(data)
#
#             except:
#                 # SNAKE DIED:
#                 gameOver = True
#                 data[1] = 1
#                 gameHistory.append(data)
#
#             directionChoice = randint(0, 3)
#
#             n += 1
#
#         with open('../data_collection/output.csv', mode='a', newline='') as file:
#             # Create a CSV writer object
#             writer = csv.writer(file)
#             for move in gameHistory:
#                 writer.writerow(move)
#
#         print(gameHistory)