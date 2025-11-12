import numpy as np


class State:
    def __init__(self, initial_probs, emission_probs, trans_probs, name):
        self.initial_probs = initial_probs
        self.emission_probs = emission_probs
        self.trans_probs = trans_probs
        self.name = name



def create_states(initial_probs, emission_probs, trans_probs):
    '''
    Purpose - Create all State objects

    Inputs -
        initial probabilities (dict of floats)
        emission probabilities (dict of floats)
        transition probabilities (dict of floats)
    Output -
        a list of States (list of object)
    '''
    states = []

    for key in initial_probs.keys():
        key = State(initial_probs[key], emission_probs[key], trans_probs[key], key)
        states.append(key)
    
    return states



def calc_sum(states, current_state, observation, previous_probs):
    '''
    Purpose - calculate the sum of the probabilities of the current observation in the current state given each possible previous state.

    Input - 
        List of State Objects
        Current State (object)
        Observations (string)
        Previous Prob (list of floats)
    Output - 
        Sum of the probabilities of the sequence of observations (float)
    '''
    probabilities = []

    for i in range(len(previous_probs)):
        probabilities.append(previous_probs[i] * states[i].trans_probs[current_state.name] * current_state.emission_probs[observation])
    
    probs_sum = sum(probabilities)

    return probs_sum



def forward_algorithm(states, observations):
    """
    Calculate the probability of the observations given the HMM.

    Inputs:
        states: list of State objects
        observations: string of observations

    Outputs:
        forward_probs: NumPy array of probabilities
        seq_prob: total probability of the observation sequence
    """

    hmm_matrix = np.zeros((len(states), len(observations)))

    initial_obs = observations[0]
    for i, state in enumerate(states):
        hmm_matrix[i, 0] = state.initial_probs * state.emission_probs[initial_obs]

    # Recursion step
    for i in range(1, len(observations)):
        for j, current_state in enumerate(states):
            hmm_matrix[j, i] = calc_sum(states, current_state, observations[i], hmm_matrix[:, i-1])

    # Sequence probability
    sequence_prob = np.sum(hmm_matrix[:, -1])
    return hmm_matrix, sequence_prob



def backward_algorithm(states, observations):
    """
    Calculate the probability of the sequence of observations
    given the HMM, moving backwards.

    Inputs:
        states: list of State objects
        observations: string of observations

    Outputs:
        backward_probs: NumPy array of probabilities
        seq_prob: total probability of the observation sequence
    """
    backward_probs = np.zeros((len(states), len(observations)))

    # Initialization step
    backward_probs[:, -1] = 1
    
        # Recursion step
    for i in range((len(observations)) - 2, -1, -1):
        for j, current_state in enumerate(states):
            backward_probs[j, i] = calc_sum(states, current_state, observations[i+1], backward_probs[:, i+1])

    # Sequence probability
    seq_prob = 0.0
    first_obs = observations[0]
    for i, state in enumerate(states):
        seq_prob += state.initial_probs * state.emission_probs[first_obs] * backward_probs[i, 0]

    return backward_probs, seq_prob



def forward_backward_algorithm(position, state, observations, states_list):
    '''
    Purpose:
    Calculate the posterior probability that the model was in a specific state at a specific position in the observation sequence
    
    Inputs -
    position: Index of the observation of interest
    state: The name of the state of interest
    observations: The entire sequence of observations
    states_list: The list of all State objects
    
    Outputs -
    the probability that the observation at the position of interest is in the state of interest (float)
    '''

    forward_matrix, forward_prob = forward_algorithm(states_list, observations)
    backward_matrix, backward_prob = backward_algorithm(states_list, observations)

    state_names = []
    for i in range(len(states_list)):
        state_names.append(states_list[i].name)
    
    for i, name in enumerate(state_names):
        if name == state:
            state_index = i

    state_prob = (forward_matrix[state_index, position] * backward_matrix[state_index, position]) / backward_prob

    return state_prob




def main():
    initial_probs = {"I": 0.1, "G": 0.9}
    emission_probs = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}, "G": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4}}
    trans_probs = {"I": {"I": 0.6, "G": 0.4}, "G": {"I": 0.1, "G": 0.9}}
    observations = "ACGCGATC"

    states = create_states(initial_probs, emission_probs, trans_probs)

    #print(calc_sum(states, states[11], "C", [0.01, 0.36]))
    #print(forward_algorithm(states, observations))
    #print(backward_algorithm(states, observations))

    print(forward_backward_algorithm(7, "G", observations, states))


if __name__ == "__main__":
   main()
