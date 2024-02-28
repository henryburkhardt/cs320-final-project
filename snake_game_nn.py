from tensorflow import keras
import snake_game
import numpy as np

loaded_model = keras.saving.load_model("mvp_nn_1.keras")

SHOW_GUI = True 
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

game = snake_game.SnakeGame(gui=SHOW_GUI, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
game.start()

gameOver = False 
while not gameOver:
    state = game.generate_vision_array()
    # print(state)
    pred = loaded_model.predict([state])
    choice = np.argmax(pred)
    try:
        game.step(choice)
    except:
        gameOver = True
        print("game over")
    
