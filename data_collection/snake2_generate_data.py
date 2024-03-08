import sys
import numpy as np
import csv
from tqdm import tqdm

sys.path.append('..')
from game import snake_game_2


def generate_row(observation: np.ndarray, direction_choice: int, game_over: int):
    return np.concatenate([observation, [direction_choice], [game_over]])


def game_loop(limit_moves, use_logic=False, use_gui=False):
    game_history = []
    game = snake_game_2.Game(gui_enabled=False)

    n_moves = 0

    move_killed_snake = False

    while (not move_killed_snake) and n_moves <= limit_moves:
        direction_choice = np.random.choice([-1, 0, 1])
        obs = np.array(game.generate_observation())

        if use_logic:
            possible_directions = np.where(obs == 0)[0]
            direction_choice = np.random.choice(possible_directions) - 1

        game.change_direction_choose(direction_choice)
        game.move()

        move_killed_snake = obs[direction_choice] == 1

        move_row = generate_row(obs, direction_choice, move_killed_snake)
        game_history.append(move_row)
        n_moves += 1
    return game_history


def clear_csv(filename):
    with open(filename, 'w') as file:
        pass


def write_head_to_csv(filename):
    header = ['obstacleL', 'obstacleF', 'obstacleR', 'direction_choice', 'game_over']
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)


def write_game_to_csv(filename, game_history):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for move in game_history:
            writer.writerow(move)


def play_games_with_logic(num_games, f):
    print("Playing {} games with logic...".format(num_games))
    for i in tqdm(range(num_games)):
        current_game_history = game_loop(use_logic=True, limit_moves=100, use_gui=False)
        write_game_to_csv(f, current_game_history)


def play_games_with_random(num_games, f):
    print("Playing {} games with random guess...".format(num_games))
    for i in tqdm(range(num_games)):
        current_game_history = game_loop(use_logic=False, limit_moves=100, use_gui=False)
        write_game_to_csv(f, current_game_history)


if __name__ == "__main__":
    f = './snake2_game_output.csv'
    clear_csv(f)
    write_head_to_csv(f)
    play_games_with_logic(300, f)
    play_games_with_random(300, f)
