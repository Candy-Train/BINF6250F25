## Viterbi Algorithm for Hidden Markov Models

Your group will demonstrate your understanding of Hidden Markov Models by implementing the Viterbi algorithm for finding the most likely sequence of hidden states given a sequence of observations.

The Viterbi algorithm represents a dynamic programming approach to decoding hidden states, offering several advantages over naïve approaches:

**Key Features**

- **Optimal Path Finding**: Identifies the most probable sequence of hidden states
- **Dynamic Programming**: Uses efficient tabulation to avoid redundant calculations
- **Log-Space Computation**: Prevents numerical underflow with large sequences
- **Traceback Mechanism**: Reconstructs the optimal state path after computation

**Algorithm Structure**

The Viterbi algorithm involves these key steps:

1. **Initialization**:
    - Set up a probability matrix using initial probabilities and the first observation
    - Initialize traceback matrix for path reconstruction
2. **Recursion**:
    - For each position and possible state, calculate the maximum probability
    - Store both probabilities and traceback pointers
    - Apply transition and emission probabilities at each step
3. **Termination**:
    - Identify the final state with the highest probability
    - Trace back through the matrix to reconstruct the optimal path

**Applications Beyond Sequence Analysis**

While primarily used for biological sequence analysis, this approach has broader applications:

- **Speech Recognition**: Identifying phonemes in audio signals
- **Part-of-Speech Tagging**: Determining grammatical roles in text
- **Gene Finding**: Locating coding regions in DNA sequences
- **Financial Modeling**: Detecting market regimes in time series data

**Computational Considerations**

Important factors to consider in implementation:

- **Time Complexity**:

where is sequence length and- is number of states
- **Space Complexity**:

- for storing the dynamic programming matrix
- **Numerical Stability**: Using log probabilities to prevent underflow
- **Edge Cases**: Handling zero probabilities with pseudocounts

**Example Data Structures**

### Example observation sequence
obs = "GGCACTGAA"
### Example initial probabilities
(probability of starting in each state)
init_probs = {"I": 0.2,    "G": 0.8}
### Example transition probabilities
(probability of moving from one state to another)
trans_probs = {"I": {"I": 0.7, "G": 0.3},    "G": {"I": 0.1, "G": 0.9}}
### Example emission probabilities
(probability of observing a symbol in a given state)
emit_probs = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}, "G": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}}

This implementation provides hands-on experience with fundamental concepts in probabilistic modeling while dealing with real genomic sequence data.

> **Notes to consider:**
> 
> - You will only be given these four data structures
> - No other template code or coding-by-contract will be provided
> - It may benefit you to utilize Object-Oriented Programming (OOP) as you will be developing out the complete HMM suite throughout the HMM modules
> - Make no assumptions as to the number of hidden states you will be given
> - Make no assumptions as to the number of distinct observations you will be given
> - Make no assumptions that the data structures will be modeling CpG islands (these were just examples)


## State Class

initial = holds the initial probability of the state (float)
emissions = holds the emission probabilities for each emission in the state (dict)
transitions = holds the transition probabilities for each transition from the state (dict)

Example - Cpg.emissions(A) would be 0.1


1. **Initialization**:
    - Set up a probability matrix using initial probabilities and the first observation
    - Initialize traceback matrix for path reconstruction
2. **Recursion**:
    - For each position and possible state, calculate the maximum probability
    - Store both probabilities and traceback pointers
    - Apply transition and emission probabilities at each step
3. **Termination**:
    - Identify the final state with the highest probability
    - Trace back through the matrix to reconstruct the optimal path

### Function 01 - Construct Probability Matrix
Purpose - Constructs a probability matrix from a list of states and and observations.

Inputs - States (list of objects), Observations (string)

Output - a probability matrix (array)

**Pseudocode**
Initialize and empty matrix of i by j where i is the number of states and j is the number of observations.
Initialize a second matrix of the same size to use as the traceback matrix.
For each state, calculate the probability of the initial state and first observation.
For each observation, use the calc_max to get the max probability and traceback matrix values


## Function 02 - Calculate the Max Probability for a Cell
Initialisation (i=0): v0(0) = 1, vk(0)=0 for k>0  
Recursion (i=1...L): vl(i) = el(xi) * maxk(vk(i–1)akl)  
ptri(l) = argmaxk(vk(i-1)akl)  
Termination: P(x,π*) = maxk(vk(L)ak0)  
πL* = argmaxk(vk(L)ak0)  
Traceback (i=L...1): πi-1* = ptri(πi*)

Purpose - Calculates the probability of the current observation in a given state, given each possible previous state.

Inputs - 
	States (list of objects)
	Probabilities of previous observation in each state (list of float)
		This can be a list of floats pulled from the previous column of our probability matrix
Output -
	The max probabilities for the observation in a state (float)
	The row of previous state that this max came from, to give to the traceback matrix (int)
## Function 03 - Traceback
Purpose - Construct the maximal path through states

Inputs -
	traceback matrix (array of ints)
	observations (string)
	row of the final state (int)
Output -
	list of state changes (list of strings)

## Function 04 - Create the State Objects
Purpose - Create a State object

Inputs -
	initial probability (float)
	emission probabilities (dict of floats)
	transition probabilities (dict of floats)
Output -
	a State (object)