# CS320 Final Project Write Up
Henry Burkhardt and Riaz Kelly
## Abstract 
In an attempt to better understand how machine learning models are able to dominate the best human players at complex games, we made three of our own machine learning models to play the game snake. Our first model was a simple ML model that kept the snake alive with 100 percent accuracy. We had mixed success with the reinforcement learning algorithms. The Q Learning algorithm was able to average up to 10 points a game. While this is not great compared to human levels, the high score of the model over 10,000 epochs was similar to the high score of a human player. ==ADD PART ABOUT OTHER NN MODEL.==
## Introduction 
We are both very interested in how computers learn to beat the human players in complex games like chess and go. Machine learning models are able to crush the best human players that have studied these games their whole lives. To gain a better understanding of how these algorithms work, we tried implementing three versions of machine learning models to play the game snake. We aim to first make a model that stays alive and then make a model that is capable of achieving a higher score than most human players. For the second model, we made two different implementations, one using a neural network and the other using Q Learning.
## Related Work 
- [Reinforcement Learning, An Introduction](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf) (freely available Stanford textbook): this in depth book, written by two of the pioneers of reinforcement learning will be a great resource for everything reinforcement learning. 
- [Playing Ms. Pacman using Advanced Neural Networks](https://fse.studenttheses.ub.rug.nl/14915/1/AI_BA_2017_AJTENCAAT.pdf) (undergrad paper): while not about Snake, I thought this paper gave a great digestible breakdown on how to create game-playing agents with reinforcement learning. It gives an excellent breakdown of rewarding models, and designing neural network inputs based on a game. It also referenced Q-learning (see below). 
- [Q-Learning Introduction](https://www.datacamp.com/tutorial/introduction-q-learning-beginner-tutorial) (tutorial website): many sources we found referenced the idea of Q learning; a popular method of rewarding/penalizing a model in the context of a game. Q-Learning allows us to use back-propagation even when our optimization function is nondifferentiable. This site is a great introduction to the topic. This will help us design our optimization function. 
- [Example of Snake Playing Neural-Net](https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3) (blog): in this blog post, the author gives a high-level overview (not providing code, just talking about concepts) on how he trained a NN to play Snake. This example is very simple, and doesn’t include Q-learning or any more complex reinforcement learning techniques. This is a good starting point for our MVP.
## Dataset 
Since we used a reinforcement learning approach, our model created its own data. We made algorithms that iteratively played snake, so every iteration added a data point. However, for the neural network RL model, we did introduce some human data at the start to accelerate the learning process. This data consisted of ~700 game moves, each move consisting of 5 features indicating obstacles around the snake, it's chosen direction, and whether or not going in this direction killed the snake. We talk more about how each model developed data in the methods section
## Methods 
### First Algorithm

Our first algorithm was simply meant to keep the snake alive. We used a neural network with 4 inputs, one hidden layer of 5 nodes, and one output node. The inputs represented if there was danger to the left, right, or straight ahead of the snake, as well as the suggested action and whether or not the snake died. The output represented how good of an action this was given the state (0 if it would keep the snake alive, 1 if it would kill the snake). This model reached 100% accuracy on the training set of computer-played gamed.  
### Neural Network Algorithm
more here...
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

