import numpy as np
from tensorflow import keras

import sys

sys.path.append("..")

from game import snake_game_2

# load saved NN that was trained on colab
loaded_model = keras.saving.load_model("exported_models/model2_possible.keras")

game = snake_game_2.Game(gui_enabled=True)


def angle_between_two_points(p1: np.array, p2: np.array):
    # Calculate the dot product of the two vectors
    dot_product = np.dot(p1, p2)

    # Calculate the magnitudes of the vectors
    magnitude1 = np.linalg.norm(p1)
    magnitude2 = np.linalg.norm(p2)

    # Calculate the cosine of the angle between the vectors
    cosine_angle = dot_product / (magnitude1 * magnitude2)

    # Calculate the angle in radians
    angle_radians = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    # Convert radians to degrees
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees


def game_loop_GUI():
    # generate observation from game to feed into NN
    obs = game.generate_observation()
    food_location = np.array([game.get_food_coordinates()[0], game.get_food_coordinates()[1]])
    head_location = game.get_snake_head_coordinates()

    scores = []

    for d in [-1, 0, 1]:
        next_head_location = np.array(game.get_next_head(d))
        print(next_head_location, food_location)
        food_angle = angle_between_two_points(next_head_location, food_location) / 180

        state = np.concatenate([obs, [d], [food_angle]]).reshape((1, 5))

        score_prediction = loaded_model.predict(state, verbose=0)

        scores.append(score_prediction)

    scores = np.round(scores)
    direction_choice = np.random.choice(np.where(scores < 1)[0]) - 1

    game.change_direction_choose(direction_choice)

    game.move()

    # logic to run the GUI and show game
    game.canvas.delete("all")
    game.canvas.create_rectangle(game.food.x, game.food.y, game.food.x + game.TILE_SIZE, game.food.y + game.TILE_SIZE,
                                 fill='red')
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


if __name__ == "__main__":
    play_with_GUI()

# %%
