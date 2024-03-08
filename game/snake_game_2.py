import tkinter
import random
import numpy as np
import csv


# global utility functions
def turn_vector_to_the_left(vector):
    """Turn vector left"""
    return np.array([-vector[1], vector[0]])


def turn_vector_to_the_right(vector):
    """Turn vector right"""
    return np.array([vector[1], -vector[0]])


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, gui_enabled):
        self.GUI_enabled = gui_enabled
        self.ROWS = 25
        self.COLS = 25
        self.TILE_SIZE = 25

        self.WINDOW_WIDTH = self.TILE_SIZE * self.COLS  # 25*25 = 625
        self.WINDOW_HEIGHT = self.TILE_SIZE * self.ROWS  # 25*25 = 625

        # GAME parameters
        self.snake = Tile(self.TILE_SIZE * 5, self.TILE_SIZE * 5)  # single tile, snake's head
        self.food = Tile(self.TILE_SIZE * 10, self.TILE_SIZE * 10)
        self.velocityX = 1
        self.velocityY = 0
        self.snake_body = []  # multiple snake tiles
        self.game_over = False
        self.score = 0

        # GUI parameters (not important):
        # game window
        if self.GUI_enabled:
            self.window = tkinter.Tk()
            self.window.title("Snake")
            self.window.resizable(False, False)

            self.canvas = tkinter.Canvas(self.window, bg="black", width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT,
                                         borderwidth=0, highlightthickness=0)
            self.canvas.pack()
            self.window.update()

            # center the window
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()

            window_x = int((screen_width / 2) - (window_width / 2))
            window_y = int((screen_height / 2) - (window_height / 2))

            # format "(w)x(h)+(x)+(y)"
            self.window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    def change_direction_keystroke(self, e):  # e = event
        """Change direction of snake from user keyboard input"""

        # global velocityX, velocityY, game_over
        if (self.game_over):
            return  # edit this code to reset game variables to play again

        if (e.keysym == "Up" and self.velocityY != 1):
            self.velocityX = 0
            self.velocityY = -1

        elif (e.keysym == "Down" and self.velocityY != -1):
            self.velocityX = 0
            self.velocityY = 1

        elif (e.keysym == "Left" and self.velocityX != 1):
            self.velocityX = -1
            self.velocityY = 0

        elif (e.keysym == "Right" and self.velocityX != -1):
            self.velocityX = 1
            self.velocityY = 0

    def change_direction_choose(self, direction):
        """
        Change the direction of the snake from input direction

        Direction should be one of the following integers:
        -1: left
        0: forward
        1: right

        Note: Direction is from the point of view of the snake. Not absolute to the board.
        """

        currentDirection = self.get_snake_direction_vector()
        newDirection = []

        if direction == -1:
            newDirection = turn_vector_to_the_left(currentDirection)
        elif direction == 0:
            newDirection = currentDirection
        elif direction == 1:
            newDirection = turn_vector_to_the_right(currentDirection)

        self.velocityX = newDirection[0]
        self.velocityY = newDirection[1]

    def move(self):
        """Execute one frame of the game"""

        if self.game_over:
            return

        headx = self.get_snake_head_coordinates()[0]
        heady = self.get_snake_head_coordinates()[1]

        x_max = self.ROWS
        y_max = self.COLS

        # check if snake has collided with the boundaries of the board
        if headx < 0 or headx > x_max or heady < 0 or heady > y_max:
            self.game_over = True
            return

        # check if snake has collided with itself
        for tile in self.snake_body:
            if self.snake.x == tile.x and self.snake.y == tile.y:
                self.game_over = True
                return

        # check if snake has collided with food
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.snake_body.append(Tile(self.food.x, self.food.y))
            self.food.x = random.randint(0, self.COLS - 1) * self.TILE_SIZE
            self.food.y = random.randint(0, self.ROWS - 1) * self.TILE_SIZE
            self.score += 1

        # update snake body
        for i in range(len(self.snake_body) - 1, -1, -1):
            tile = self.snake_body[i]
            if i == 0:
                tile.x = self.snake.x
                tile.y = self.snake.y
            else:
                prev_tile = self.snake_body[i - 1]
                tile.x = prev_tile.x
                tile.y = prev_tile.y

        # move head of snake
        self.snake.x += self.velocityX * self.TILE_SIZE
        self.snake.y += self.velocityY * self.TILE_SIZE

    def get_snake_head_coordinates(self):
        """Get coordinates of snake head"""
        return self.snake.x / self.ROWS, self.snake.y / self.COLS

    def get_snake_body_coordinates(self):
        """Get coordinates of all snake tiles excluding the head"""
        return [(tile.x / self.ROWS, tile.y / self.COLS) for tile in self.snake_body]

    def get_snake_coordinates(self):
        """Get coordinates of all snake tiles"""
        snake_head = self.get_snake_head_coordinates()
        snake_body = self.get_snake_body_coordinates()
        return snake_head, snake_body

    def get_snake_direction_vector(self):
        """Get velocity vetor for head of the snake"""
        return [self.velocityX, self.velocityY]

    def is_direction_blocked(self, direction):
        """Check if cell in a given direction is empty or not"""
        point = np.array(self.get_snake_head_coordinates()) + np.array(direction)
        return (point.tolist() in self.get_snake_body_coordinates() or point[0] == 0 or point[1] == 0
                or point[0] == self.ROWS or point[1] == self.COLS)

    def generate_observation(self):
        """Check all 3 cells surounding the snake (all possible cells it could travel to) for barriers
        :returns binary array of length three: [barrier_left, barrier_front, barrier_right]
        """
        snake_direction = self.get_snake_direction_vector()
        barrier_left = self.is_direction_blocked(turn_vector_to_the_left(snake_direction))
        barrier_front = self.is_direction_blocked(snake_direction)
        barrier_right = self.is_direction_blocked(turn_vector_to_the_right(snake_direction))
        return np.array([int(barrier_left), int(barrier_front), int(barrier_right)])

#
# def generate_row(observation: list, direction_choice: int, game_over: int):
#     return np.concatenate([observation, [direction_choice], [game_over]])
#
#
# def game_loop(limit_moves, use_logic=False, use_gui=False):
#     game_history = []
#     game = Game(gui_enabled=use_gui)
#
#     n_moves = 0
#
#     move_killed_snake = False
#
#     while (not move_killed_snake) and n_moves <= limit_moves:
#         if game.game_over: print("GAME OVER")
#         direction_choice = np.random.randint(0, 3)
#         obs = np.array(game.generate_observation())
#
#         if use_logic:
#             possible_directions = np.where(obs == 0)[0]
#             direction_choice = np.random.choice(possible_directions)
#
#         game.change_direction_choose(direction_choice)
#         game.move()
#
#         move_killed_snake = obs[direction_choice] == 1
#
#         move_row = generate_row(obs, direction_choice, move_killed_snake)
#         game_history.append(move_row)
#         # print(move_row)
#         n_moves += 1
#     return game_history
#
#
# def clear_csv(filename):
#     with open(filename, 'w') as file:
#         pass
#
#
# def write_head_to_csv(filename):
#     header = ['obstacleL', 'obstableF', 'obstacleR', 'direction_choice', 'game_over']
#     with open(filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#
#
# def write_game_to_csv(filename, game_history):
#     with open(filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         for move in game_history:
#             writer.writerow(move)
#
#
# def play_games_with_logic(num_games, f):
#     for i in range(num_games):
#         current_game_history = game_loop(use_logic=True, limit_moves=100, use_gui=False)
#         write_game_to_csv(f, current_game_history)
#         print("Game ", i, " complete")
#
#
# def play_games_with_random(num_games, f):
#     for i in range(num_games):
#         current_game_history = game_loop(use_logic=False, limit_moves=100, use_gui=False)
#         write_game_to_csv(f, current_game_history)
#         print("Game ", i, " complete")
#
#
# if __name__ == "__main__":
#     f = '../data_collection/snake2_game_output.csv'
#     clear_csv(f)
#     write_head_to_csv(f)
#     play_games_with_logic(300, f)
#     play_games_with_random(300, f)
