from tensorflow import keras
from game import snake_game
import numpy as np

loaded_model = keras.saving.load_model("./models/possible_mvp.keras")

SHOW_GUI = True
BOARD_WIDTH = 15
BOARD_HEIGHT = 15

game = snake_game.SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
game.start()

gameOver = False
while not gameOver:
    visionState = game.generate_vision_array()
    direction_scores = []
    for i in range(0, 4):
        direction = [0, 0, 0, 0]
        direction[i] = 1
        state = np.array([direction + visionState])
        state = state.reshape((1,8))
        print(state)
        # pred = loaded_model.predict(state, verbose=0)
        # direction_scores.append(pred)

    # best_direction = np.argmax(direction_scores, axis=0)
    # print(best_direction)
    # try:
    #     game.step(best_direction)
    # except:
    #     gameOver = True
    #     # print("game over")
