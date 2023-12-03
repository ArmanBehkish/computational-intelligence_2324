# LAB 9 
### version 1.13

The code implements a GA that can adapt for different problem sizes. The main characteristics of the code is:

 - It has a mutation with configurable number of bits to flip, uniform crossover, or crossover (logical OR), and n-cut crossovers with configurable n.
 - There is a fitness memory (dict) that keeps track of the fitness of individuals to avoid calling fitness routine.
 - There is a probability distribution with a specific probability for each genetic operator. In each round to create offspring, the operator is selected using this probability distribution. If the maximum fitness achieved is constant for a number of generations, the probibility distribution is mutated using guassian mutation with configurable sigma, so that the algorithm can adapt the genetic operation used.
 - the best individuals in each generation is kept in VALHALA to copy to next generation, so that algorithm won't lose the champions.
 - as a sample result:
   - for problem size 2, 70% fitness can be reached with fitness calls as low as 6755.
   - for problem size 10 is 0.20677778 with 7820 calls


