# CS320 Final Project Write Up
Henry Burkhardt and Riaz Kelly
## Abstract 
In an attempt to better understand how machine learning models are able to dominate the best human players at complex games, we made three of our own machine learning models to play the game snake. Our first model was a simple ML model that kept the snake alive with 100 percent accuracy. We had mixed success with the reinforcement learning algorithms. The Q Learning algorithm was able to average up to 10 points a game. While this is not great compared to human levels, the high score of the model over 10,000 epochs was similar to the high score of a human player. We ambitiously also tried to train our simple survival network to play the game better, but unfortunately we ran out of time perfecting this model. It has still been included to show the work we did on it, and we believe given more time for training and hyper-paramter tuning it could outplay most humans. 
## Introduction 
We are both very interested in how computers learn to beat the human players in complex games like chess and go. Machine learning models are able to crush the best human players that have studied these games their whole lives. To gain a better understanding of how these algorithms work, we tried implementing three versions of machine learning models to play the game snake. We aim to first make a model that stays alive and then make a model that is capable of achieving a higher score than most human players. For the second model, we made two different implementations, one using a neural network and the other using Q Learning.
## Related Work 
The two resources below provide to different approaches to creating intelligent game-playing agents with machine learning. We consulted both of these resources heavily to influence our own approach. 
- [Playing Ms. Pacman using Advanced Neural Networks](https://fse.studenttheses.ub.rug.nl/14915/1/AI_BA_2017_AJTENCAAT.pdf) (undergrad paper): while not about Snake, this paper details playing a computer game with reinforcement learning. These researchers implement deep-Q learning (where a policy is encoded in a nerual network) to successfully play the game. This was our original inspiration to use Q-learning in our models. 
- [Example of Snake Playing Neural-Net](https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3) (blog): in this blog post, the author gives a high-level overview (not providing code, just talking about concepts) on how he trained a NN to play Snake. This example is very simple, and doesn’t include Q-learning or any more complex reinforcement learning techniques. This is a good starting point for our MVP, and shows that sometimes simple games can be learned by simply providing enough random input data. 
Note that these two are just the tip of a very, very large iceberg. Game playing agents built with RL has been an incredibly generative field of research in the past 10+ years, and there are many many different ways of approaching the problem. After a lot of research though, we are confident are methodology is the most reasonable starting point for our objective. 
## Datasets
Since we used a reinforcement learning approach, our model created its own data. We made algorithms that iteratively played snake, so every iteration added a data point. However, for the neural network RL model, we did introduce some human data at the start to accelerate the learning process. This data consisted of ~700 game moves, each move consisting of 5 features indicating obstacles around the snake, it's chosen direction, and whether or not going in this direction killed the snake. We talk more about how each model developed data in the methods section
## Methods 
### Simple NN Algorithm 
Our first algorithm was simply meant to keep the snake alive. We used a neural network with 4 inputs, one hidden layer of 5 nodes, and one output node. The inputs represented if there was danger to the left, right, or straight ahead of the snake, as well as the suggested action and whether or not the snake died. The output represented how good of an action this was given the state (0 if it would keep the snake alive, 1 if it would kill the snake). This model reached 100% accuracy on the training set of computer-played gamed.  

The training data was generated using the `neural_network/data_collection/snake_game_2_generate_data.py` script. This script plays 600 games of snake. In half of the games, the snake makes a random decisions which direction to turn every frame. In the other half the snake is programmed to always avoid collisions. Thus, our training data will include both positive and negative examples. 
### Complex NN Algorithm
This neural network is designed to drive the snake towards food, as well as not ending its life. To achieve this we added another node to the NN that encodes the angle between the snake and the food tile. The hope is that the NN can learn from training that moves with a smaller angle between itself and food are favorable. To achieve this, we interface the NN with game, and add a custom loss function that penalizes the model for making guesses that drive it away from the food tile so long as it isn't running into an obstacle.
### Q Learning Algorithm

Q Learning is a reinforcement learning algorithm that has rewards and punishments for different actions. Iteratively, the model learns how to chase rewards and avoid punishments. This is done using a Q Table, which represents every possible action at every possible game state. We could have defined every possible game state using the whole board, but this felt like overkill. Instead, we chose 11 binary inputs to represent all game states in a concise but relevant way. 

1. Is there danger to the left of the head of the snake?
2. Is there danger to the right of the head of the snake?
3. Is there danger straight ahead of the head of the snake?
4. Is the snake currently going north?
5. Is the snake currently going east?
6. Is the snake currently going south?
7. Is the snake currently going west?
8. Is the food north of the snake?
9. Is the food east of the snake?
10. Is the food south of the snake?
11. Is the food west of the snake?

  Since these are all binary, we have 211= 2048 game states. At any moment, the snake can go left, right, or stay in its current direction. We then have a Q Table with dimensions 2048 x 3. We chose to have three rewards/punishments for the snake. We have + 10 if it ate food, – 10 if it died, and + 1 if it got closer to the food. 

Now the big question is what formula do we use to update values in the Q Table? We use a simplified version of the most common update equation for Q Learning:

$$Q(\texttt{State}, \texttt{Action}) = (1 - ) Q(\texttt{State}, \texttt{Action}) + (\text{reward}+ ((\text{max}(Q(\texttt{New State}, \texttt{Possible Actions}))$$

Where Q(State, Action) is the Q Table value at a given state and action and max(Q(New State, Possible Actions) is the maximum Q Table value of the new game state given all possible actions. The values alpha and gamma are hyperparameters representing the learning rate (how fast the model learns) and discount factor (how much the model weights rewards). We then used the following loop to train our Q Learning Model:
- Choose an action
- Random if all Q Table action values are 0
- Maximum of the Q Table action values if not 0
- Perform action and get the reward
- Update the Q Table based on the update equation
- Repeat

Using this loop, we tested various values of alpha and gamma to maximize the model’s score.
## Experiments and Results 
### Simple NN Algorithm (model_1)
After 40 training epochs on our game data, the snake stayed alive with 100 percent accuracy. This was expected as the snake had a very simple goal. Additionally, the snake is much more likely to run into itself and die as it gets bigger, but with this algorithm, it didn’t get bigger unless it collided with a food tile by random chance. 

We selected the learning rate and bath size based on our trial and error. The relationship in the underlying data is so simple that we did not even need to implement cross validation to find the most optimal parameters.
### Complex NN Algorithm (model_2)
Experimentally, the complex NN did not perform well like we expected it to. It appears to have about the same attraction to food as model_1. I believe this is due to a weighting issue in our loss function, and a lack of training data. It takes about 1 minute right now for the model to play just 10 games, with a limit of 30 moves each. For this reason, it's proven hard to get the model trained. If we had more time this is something we'd prioritize early on in the project. The code, and architecture of model_2 is still all available, and demonstrates the amount of work that we put in trying to get this model to function. We could not get this model to be completely functional, so the hyper parameters are still int the process of being tuned. We have been manually adjusting them, looking at training and testing accuracy to guide us. 
### Q Learning Algorithm
After about 100 – 200 iterations, the model reached a “plateau” score, averaging 8 – 9 points a game. We found that changing alpha and gamma had negligible effect on the outcome. While the model didn’t average nearly as high of a score as we would have liked, it did reach high scores close to a hundred. This was a very positive result as it is not common for human players to reach scores close to a hundred.
## Discussion and Future Work
We learned a lot over the course of this project. It was cool to know that the approaches we learned and implemented are similar to those used by massive corporations to create AlphaGO and AlphaZero. We wanted to get better results, but needed more time to tune our models. The algorithms we learned don’t seem very complicated at face value, but in order to create truly robust models that can easily surpass a human player, we would need more time, data, and computational power. We found that the neural network approach performed better than the Q Learning algorithm. This could be due to our implementation of Q Learning, as there are many existing Q Learning algorithms that are able to get very high scores in snake. 

If we had more time we would fine tune our models and try different implementations of Q Learning (define a game state differently). As snake is a pretty simple game, future work could be implementing these techniques on progressively more complicated games. Although, this would increasingly require more computational power.

As mentioned earlier, we would also retrain model_2 on way more games so it could learn the relationships of the game bette. 

