import numpy as np
from game import snake_game_2
from tensorflow import keras

loaded_model = keras.saving.load_model("models/saved_models/model_1.keras")

game = snake_game_2.Game(gui_enabled=True)


def game_loop_GUI():
    obs = np.array(game.generate_observation())

    # possible_directions = np.where(obs == 0)[0]
    # direction_choice = np.random.choice(possible_directions)

    ## NN logic here

    scores = []
    # adjusting for new direction architecture
    for d in [-1, 0, 1]:
        state = np.concatenate([obs, [d]]).reshape((1, 4))
        score_prediction = loaded_model.predict(state, verbose=0)
        scores.append(score_prediction)

    scores = np.round(scores)
    direction_choice = np.random.choice(np.where(scores < 1)[0]) - 1

    game.change_direction_choose(direction_choice)

    game.move()

    game.canvas.delete("all")

    # draw food
    game.canvas.create_rectangle(game.food.x, game.food.y, game.food.x + game.TILE_SIZE, game.food.y + game.TILE_SIZE,
                                 fill='red')

    # draw snake
    game.canvas.create_rectangle(game.snake.x, game.snake.y, game.snake.x + game.TILE_SIZE,
                                 game.snake.y + game.TILE_SIZE, fill='lime green')

    for tile in game.snake_body:
        game.canvas.create_rectangle(tile.x, tile.y, tile.x + game.TILE_SIZE, tile.y + game.TILE_SIZE,
                                     fill='lime green')

    if (game.game_over):
        game.canvas.create_text(game.WINDOW_WIDTH / 2, game.WINDOW_HEIGHT / 2, font="Arial 20",
                                text=f"Game Over: {game.score}", fill="white")
        print("Game Over")
    else:
        game.canvas.create_text(30, 20, font="Arial 10", text=f"Score: {game.score}", fill="white")

    if not game.game_over:
        game.window.after(100, game_loop_GUI)  # call draw again every 100ms (1/10 of a second) = 10 frames per second


def play_with_GUI():
    game_loop_GUI()
    game.window.bind("<KeyRelease>", game.change_direction_keystroke)  # when you press on any key and then let go
    game.window.mainloop()  # used for listening to window events like key presses


play_with_GUI()
