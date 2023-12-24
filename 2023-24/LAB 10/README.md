## RL for Tik Tok Toe

1. We use the following recursieve (bellman equation) formula to computer the state-value table. It is better to gratually decrease the learning parameter to the point of convergence (to be implemented in later versions).
   
$$ V(S_t) <- V(S_t) + &alpha;[V(S_t+1)-V(S_t)]$$

2. All the possible combinations for states are ara calculated and the initial state values are set to 0.5.
   
3. The RL player function chooses the next move based on best state value in the available moves. if there is not value is associated with the state, a random move is choosen.

4. A function plays given number of games between two given agents and returns the percentage wins.
