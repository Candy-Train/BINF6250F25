# Introduction
Through this program, we implement forward, backward and forward backward algorithms for hidden Markov models. These algorithsm utilize 
joint probabilites, conditional probabilities and posterior probabilities to determine past probabilities, future probabilities and 
specific probabilities depending on state and position in a sequence.

# Pseudocode
Put pseudocode in this box:

```
**State Class**

initial_probs = holds the initial probability of the state (float)
emission_probs = holds the emission probabilities for each emission in the state (dict)
trans_probs = holds the transition probabilities for each transition from the state (dict)
name = name of the state

**create_states Function**

Purpose:
Construct a list of all State objects that define the HMM

Inputs:
initial_probs: initial probabilities for each state
emission_probs: emission probabilities for each state
trans_probs: transition probabilities between states

Pseodocode:
Create an empty list called `states`
For each state name in the initial probability dictionary:
  Create a new State object using its initial, emission, and transition probabilities
  Append this state object to the states list
  Return the full list of all State objects

Output:
A list of fully constructed state objects

**calc_sum Function**

Purpose:
Compute the total probability of being in the current state

Inputs:
states: List of all State objects
current_state: The state being evaluated
observation: The observation at the current position
previous_probs: The array of probabilities from the previous time step (forward) or next time step (backward)

Pseodocode:
Create an empty list for probabilities
For each previous state:
  Multiply the previous state’s probability by:
    The transition probability from that state to the current state
    The emission probability of observation in the current state
  Append this value to the list
Sum all those values to get the total probability of reaching the current state

Output:
The summed probability for the current state and observation

**forward_algorithm Function**

Purpose:
Calculate the probability of the observations given the HMM

Inputs:
states: list of State objects
observations: string of observations

Outputs:
forward_probs: NumPy array of probabilities
seq_prob: total probability of the observation sequence
    
Pseudocode:
For each current state, call calc_sum to compute probability of that state given all previous states
Store that probability in the current cell of the HMM matrix
Sum the probabilities of the final column across all states, giving us the total probability of observing the whole sequence
Return full matrix and total sequence probability

**backward_algorithm Function**

Purpose:
Calculate the probability of the sequence of observations given the HMM, moving backwards

Inputs:
states: list of State objects
observations: string of observations

Outputs:
backward_probs: NumPy array of probabilities
seq_prob: total probability of the observation sequence
    
Pseodocode:
Create zero matrix to hold backward probabilities
Set last column to all ones
Working backward through the sequence, we use the same calculations for the forward algorithm, but backwards rather than forwards
Sum the probabilities over all states, and store those in the backward matrix
Calculate the total probability, and sum across all states
Return both backward matrix and total sequence probability

**forward_backward_algorithm Function**

Purpose:
Calculate the posterior probability that the model was in a specific state at a specific position in the observation sequence

Inputs:
position: Index of the observation of interest
state: The name of the state of interest
observations: The entire sequence of observations
states_list: The list of all State objects

Outputs:
the probability that the observation at the position of interest is in the state of interest (float)

Process:
Run the forward algorithm to get the forward probability matrix and total sequence probability
Run the backward algorithm to get the backward probability matrix and total sequence probability
Find the index of the state of interest in the states list
Compute the posterior probability for that state and position

Output:
The posterior probability of being in that state at that position
```

# Successes
We were able to use some of what we wrote for Project 08 to get us through this program, which was fairly straightforward to write.
We produced probabilities that (mostly) make sense to us for each of the algorithms. 


# Struggles
We did have some issues getting the forward and backward algorithms to produce probabilities that were close to one another. At first,
the backward probability that we were producing was off by a factor of at least 10, but we were able to reduce that. We still were not 
able to get them to exactly match, but there is a smaller discrepancy now. We also found some conflicting equations online for 
calculating the posterior probability, but are sticking with what the lecture notes told us. 

# Personal Reflections
## Group Leader - Chris
Overall, this went smoothly. We had a solid understanding of what we needed to do, and how to achieve it, right up until the forward-backward algorithm. We found that if we used the total probability from the foward algorithm in the denominator, that the results were more accurate for observations earlier in the sequence. But if we used the backward algorithm probability, later observations were more accurate. 

## Other member - Abi
I think that this was a fairly simple program to write. We were able to use bits and pieces from Porject 08, but did wind up changing
some things. I got a bit mixed up with the backward algorithm, which was why we were getting weird probabilities, but that was a fairly
quick fix.

# Generative AI Appendix
No AI was used.
