LAB 2: EVOLUTIONARY ALGORITHM IMPLEMENTATION FOR NIM GAME
=========================================================
***THIRD REVISION*** 
*17TH NOV*

In this implementaion, I implemented a class to perform ES (&lambda; + 1) stragegy. 

- **Presentation**: the presentation chosen for this implementation is a dictionary in which the keys are tuples in the form of Nimply and the values are probabilities. The keys are all possible moves the agent can perform in a game board, e.g., (row=2,object=3) and the probabilities form a distribution (sum to one).
- **Tweak**: the tweak is a gaussian nudge to a randomly selected item in the individual. the value of sigma (step) is set to around 20%. 
- **Fitness**: the fitness is implemented using a 100 games against the optimal opponent and the number of wins account for the fitness value.
- **Population**: the population is a list of individuals along with their fitness value. in each round the fitness is computed for all individuals and best one is selected. if the last two reounds stuck in the same top fitness, a restart is performed.
- **Exploration**: different values of &lambda; , population size, number of game for fitness, etc. were tested and it seems the best output is for large values of &lambda;. 
- **Testing**: many improvenets are possible which will be addedd gradually.
- **Adaptive Learning** a class is implemented to record and find percentage difference in fitness values. Based on the percentage change in fittness values in each loop, the sigma (step) is adjested to find a balance between exploration and exploitation.
- **Results**: The algorithm is able to easily climb to 50% wins against the optimal (nimsum) player. 
- **Best Result** : 75% win against pure_random - 100% win against gabriele
