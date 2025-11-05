# Introduction
With this program, we implement the Viterbi algorithm, which is a technique used to find the most likely sequence of hidden events that could explain a sequence of observed events. For example, a doctor observes symptoms that a patient is displaying, and the hidden states are the diagnosis that the doctor would conclude. The steps of the algorithm are initialization, recursion, and termination, which are demonstrated in the functions we created, outlined in the pseodocode below. 

# Pseudocode

```
## State Class

initial_probs = holds the initial probability of the state (float)
emission_probs = holds the emission probabilities for each emission in the state (dict)
trans_probs = holds the transition probabilities for each transition from the state (dict)
name = name of the state

Example - Cpg.emission_probs(A) would be 0.1


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
Purpose - Constructs a probability matrix from a list of states and and observations. Fills in the traceback matrix with the most probable previous state.

Inputs - States (list of objects), Observations (string)

Output - a probability matrix (array), traceback matrix (array)

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
Purpose - Create a list of State objects

Inputs -
	initial probabilities (dict of float)
	emission probabilities (dict of floats)
	transition probabilities (dict of floats)
Output -
	a list of States (list of object)
```

# Successes
This project went smoothly, we were able to use a great deal of knowledge from previous projects to complete the functions we needed. Overall, this program implemented a lot of things we already knew how to do, and came together quickly. 

# Struggles
The trickiest part of this project was breaking down the recursive equation we needed to use, and making sure that we wrote it into the function correctly. We also forgot to write it in log-space originally, but that was a quick and easy fix. (Abi)
I suspect that any struggles we have yet to notice will become more obvious as we get deeper into the project. (Chris)

# Personal Reflections
## Group Leader - Chris
This was a good start to the final project. The blank canvas can be intimidating, but I kind of like the process of breaking everything down to it's most managable piece and indentifying what functions we need and what their requirements are. We got to lean on past project knowledge, and lay the foundation for something new. Ideally, this is a solid foundation and we won't have to revist it. Plus, no more Rstudio, so my silly syntax mistakes are easy to spot now.

## Other member - Abi
I enjoyed this project, it was good to get more practice creating probability and traceback matrices, as well as some more numpy functions. I also don't have much experience using classes, so it was nice to be able to implement those as well. I liked that we had the freedom to use our choice of programming platform, and we elected to use VSCode, which I like much better than RStudio. 

# Generative AI Appendix
As per the syllabus
