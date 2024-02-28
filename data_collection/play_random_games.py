import sys
import csv
from random import randint
import numpy as np

# import game from parent directory
sys.path.append('../')
from game import snake_game

if __name__ == "__main__":
    # options:
    SHOW_GUI = False
    BOARD_HEIGHT = 10
    BOARD_WIDTH = 10
    NUM_GAMES = 1
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
            ['n', 'gameOver', 'head', 'score', 'visionUp', 'visionRight', 'visionDown', 'visionLeft',
             'directionChoice'])

    for _ in range(NUM_GAMES):
        n = 0
        gameOver = False
        gameHistory = []

        # initiate a new game
        game = snake_game.SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
        game.start()

        directionChoice = randint(0, 3)

        while not gameOver:
            # get game state info
            done, score, snake, food = game.generate_observations()
            [visionUp, visionRight, visionDown, visionLeft] = game.generate_vision_array()
            data = [n, gameOver, game.snake[0], score, visionUp, visionRight, visionDown, visionLeft, directionChoice]

            if SAVE_MATRIX:
                # Write matrix to file
                with open('matrix_output.txt', 'a') as file:
                    file.write(str("------- MOVE " + str(n) + " ------- \n"))
                    np.savetxt(file, game.board_matrix, fmt='%d', delimiter=' ', newline="\n")

            # iterate game by one step
            try:
                # SNAKE LIVES:
                game.step(directionChoice)
                data[1] = 0  # this sets the gameOver variable to false
                gameHistory.append(data)

            except:
                # SNAKE DIED:
                gameOver = True
                data[1] = 1
                gameHistory.append(data)

            directionChoice = randint(0, 3)

            n += 1

        with open('output.csv', mode='a', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)
            for move in gameHistory:
                writer.writerow(move)

        print(gameHistory)
