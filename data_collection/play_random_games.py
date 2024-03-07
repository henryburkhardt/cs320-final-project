# plays games by randomly choosing directions at each move and records the results in a cs

import sys
import csv
from random import randint
import numpy as np

# import game from parent directory
sys.path.append('../')
from game import snake_game
from game import snake_original


def generate_observation2(snake):
    print(snake)
    get_snake_direction_vector(snake)
    snake_direction = get_snake_direction_vector(snake)
    barrier_left = is_direction_blocked(snake, turn_vector_to_the_left(snake_direction))
    barrier_front = is_direction_blocked(snake, snake_direction)
    barrier_right = is_direction_blocked(snake, turn_vector_to_the_right(snake_direction))
    return np.array([int(barrier_left), int(barrier_front), int(barrier_right)])

def add_action_to_observation(observation, action):
    return np.append([action], observation)

def get_snake_direction_vector(snake):
    return np.array(snake[0]) - np.array(snake[1])

def is_direction_blocked(snake, direction):
    point = np.array(snake[0]) + np.array(direction)
    return point.tolist() in snake[:-1] or point[0] == 0 or point[1] == 0 or point[0] == 20 or point[1] == 20

def turn_vector_to_the_left(vector):
    return np.array([-vector[1], vector[0]])

def turn_vector_to_the_right(vector):
    return np.array([vector[1], -vector[0]])

def get_game_action(snake, action):
    snake_direction = get_snake_direction_vector(snake)
    new_direction = snake_direction
    if action == -1:
        new_direction = turn_vector_to_the_left(snake_direction)
    elif action == 1:
        new_direction = turn_vector_to_the_right(snake_direction)
    for pair in self.vectors_and_keys:
        if pair[0] == new_direction.tolist():
            game_action = pair[1]
    return game_action

def create_data_random(SHOW_GUI, BOARD_HEIGHT, BOARD_WIDTH, NUM_GAMES, SAVE_MATRIX, MOVE_LIMIT=1e-10):
    # clear output files
    with open('output.csv', 'w') as file:
        pass

    with open('matrix_output.txt', 'w') as file:
        pass

    # write header line to output csv
    # with open('output.csv', mode='a', newline='') as file:
    #     # Create a CSV writer object
    #     writer = csv.writer(file)
    #     # Write headers
    #     writer.writerow(
    #         ['n', 'gameOver', 'head', 'score', 'visionUp', 'visionRight', 'visionDown', 'visionLeft',
    #          'directionChoice'])

    # a nice variable to have, so we can know the total # of moves computed on a run
    total_moves = 0

    for _ in range(NUM_GAMES):
        n = 0
        gameOver = False
        gameHistory = []

        # initiate a new game
        game = snake_original.SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
        game.start()

        directionChoice = randint(0, 3)

        while (not gameOver and n < MOVE_LIMIT):
            # get game state info
            done, score, snake, food = game.generate_observations()
            # [visionUp, visionRight, visionDown, visionLeft] = game.generate_vision_array()
            # data = [n, gameOver, game.snake[0], score, visionUp, visionRight, visionDown, visionLeft, directionChoice]
            observation = np.array(generate_observation2(snake))
            # format = [barrier_L, barrier_Front, barrier_R]
            print(snake, observation)
            data = observation

            if SAVE_MATRIX:
                # Write matrix to file
                with open('matrix_output.txt', 'a') as file:
                    file.write(str("------- MOVE " + str(n) + " ------- \n"))
                    np.savetxt(file, game.board_matrix, fmt='%d', delimiter=' ', newline="\n")

            # iterate game by one step
            try:
                # SNAKE LIVES:
                game.step(directionChoice)
                data = np.append(data, 0) # this sets the gameOver variable to false
                gameHistory.append(data)

            except:
                # SNAKE DIED:
                gameOver = True
                data = np.append(data, 1)
                gameHistory.append(data)

            directionChoice = randint(0, 3)

            n += 1

        total_moves += n

        with open('output.csv', mode='a', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)
            for move in gameHistory:
                writer.writerow(move)

    print("Successfully played ", NUM_GAMES, "games, consisting of ", total_moves, " moves.")


if __name__ == "__main__":
    # options:
    create_data_random(
        SHOW_GUI=False, BOARD_HEIGHT=20, BOARD_WIDTH=20, NUM_GAMES=1, SAVE_MATRIX=True, MOVE_LIMIT=100)
