# Model Files 
This folder contains our Keras models exported to files so they can be loaded in other parts of the project. 

- `model_1`: first functional model, trained on `snake2_game_output.csv`
  - This model only avoids edges, has no other logic. It should stay alive forever though. This is the successful MVP.

- `model_2`: still needs to get made 
  - can be trained starting with model1 logic and then using re-enforcement learning with a custom loss function to get better at actually playing the game