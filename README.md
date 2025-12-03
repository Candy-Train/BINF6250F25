# Introduction
We continue building on the last two projects with this program, implementing the Baum - Welch algorithm. The Baum - Welch algorithm takes in a sequence of observations, rather than just one. This algorithm is used to estimate and update the parameters of a HMM given these observations. It relies on joint probabilities to determine the most probable parameters for the model. 

# Pseudocode

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

**baum_welch Function **


Initialize model as converged
Set up variables for total posterior probabilities per state, total expected transitions between each pair of states, total counts of emitted symbols from each state, and total posterior probabilities at the first position

For each observation sequence:
Build a dictionary that records where each symbol appears in the sequence, run forward-backward algorithm on that sequence, compute the expected number of transitions between states for each position
After running through all sequences, update initial probabilities,  emission probabilities, and transition probabilities:
For each, if the value differs from the previous by more than 0.001, mark the model as not converged
Model converges if difference is less than 0.001, or if it reaches 100 iterations (whichever occurs first)
Return the updated states and whether convergence was achieved

```

# Successes
We were able to write the two helper functions to Baum - Welch with no issues. We were also able to tweak what we did have for the main Baum - Welch function to be able to take in multiple sequences of differing lengths. We were able to build on skills and functions from the last two projects, and were able to both understand the algorithm and make a plan before going into coding. 

# Struggles
We ran into a few obstacles with this project. We spent the first week we were given just going though the equations the algorithm was going to need and making sure that we understood each of the components of the equations. Once we understood these, it was much easier to get through some coding. Towards the end of writing the main Baum - Welch function, we discovered how difficult it was going to be to correctly put the math we were doing into log - space, as well as bringing it back out at the end. Even without putting it into log - space, the results we were getting did not exactly make sense, so we suspect that some math we are doing is wrong somewhere. We went through it many times to determine what we were doing wrong, as well as going through the code that Marcus wrote, and everything looks right, but we are still getting confusing outputs. 

# Personal Reflections
## Group Leader - Chris
Group leader's reflection on the project

## Other member - Abi
I feel like I definitely have a good understanding of how the algorithm is intended to work, we were just having some issues with implementing it in the way we imagined we would be able to. I still am not the most advanced programmer in the world, so not knowing how to fix everything is admittedly frustrating, but overall, I am proud of the work that we were able to produce. 

# Generative AI Appendix
As per the syllabus
