# Source for initial code:
# 
# https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/

'''
Rather than give a whole map of the board, we will do some "preprocessing" on
the board data to give only the relevant information. Then, we will have 11 inputs in our q table:

Danger straight
Danger left
Danger right
Current Direction North
Current Direction East
Current Direction South
Current Direction West
Food North
Food East
Food South
Food West

Because each input is binary, we will have 2 ^ 11 = 2048 states in our q table. 
Since we have 3 possible actions, our q table should be of size: 2048 by 3.
'''

import numpy as np
import pandas as pd
from game import snake_game
import random
import csv
import matplotlib.pyplot as plt
from IPython.display import clear_output

SHOW_GUI = True 
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
NUM_ACTIONS = 4
FOOD_REWARD = 10
DEATH_PENALTY = -10
CLOSER_TO_FOOD_REWARD = 1

def main(alpha = 0.1, gamma = 0.6, epsilon = 0.05):

    q_table = np.zeros([2048, NUM_ACTIONS])
    scores = []
    high_score = 0
    moves = 0
    sum = 0

    for i in range(1, 10000):

        # initialize game
        game = snake_game.SnakeGame(gui=False, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT)
        vals, reward, done, score, old_distance_to_food = game.start()
        game_state = get_table_val(vals)
        done = False
        
        while not done:
            if np.sum(q_table[game_state]) == 0.0:
                action = random.randint(0, NUM_ACTIONS - 1) # Explore action space
            else:
                action = np.argmax(q_table[game_state]) # Exploit learned values
            
            vals, reward, done, score, next_distance_to_food = game.step(action)
            if reward == 0 and next_distance_to_food < old_distance_to_food:
                reward = CLOSER_TO_FOOD_REWARD

            next_state = get_table_val(vals)
            moves += 1
            
            old_value = q_table[game_state, action]
            next_max = np.max(q_table[next_state])
            
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[game_state, action] = new_value

            game_state = next_state
            old_distance_to_food = next_distance_to_food
            
        scores.append(score)
        sum += score
        if score > high_score:
            high_score = score
        if i % 100 == 0:
            clear_output(wait=True)
            print(f"Episode: {i}, Average Score: {sum / 100}")
            sum = 0

    print("Training finished.\n")
    print("Number of total moves", moves)
    print("High Score", high_score)
    return q_table, scores

def get_table_val(vals):
    sum = 0
    for i in range(0, 11):
        sum += ((2 ** i) * vals[i])
    return sum

q_table, scores = main(alpha = 0.1)

# Code to write the q_table to a csv file, but I commented it out for colab purposes

# with open("q_table.csv","w+") as my_csv:
#     csvWriter = csv.writer(my_csv,delimiter=',')
#     csvWriter.writerows(q_table)

# my_csv.close()

games = range(0, 10000, 100)
sum = 0
avg_scores = []
for i in range(len(scores) - 1):
    sum += scores[i]
    if i % 100 == 0:
        avg_scores.append(sum / 100)
        sum = 0
    

plt.plot(games, avg_scores, color="red")
plt.show()