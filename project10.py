import numpy as np
from collections import defaultdict


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
    
    # Loop step
    for i in range((len(observations)) - 2, -1, -1):
        for j, current_state in enumerate(states):
            backward_probs[j, i] = calc_sum(states, current_state, observations[i+1], backward_probs[:, i+1])

    # Sequence probability
    seq_prob = 0.0 #but why?
    first_obs = observations[0]
    for i, state in enumerate(states):
        seq_prob += state.initial_probs * state.emission_probs[first_obs] * backward_probs[i, 0]

    return backward_probs, seq_prob



def forward_backward_algorithm(states, observations):

    forward_matrix, forward_prob = forward_algorithm(states, observations)
    backward_matrix, backward_prob = backward_algorithm(states, observations)

    posterior_prob_matrix = np.zeros((len(states), len(observations)))
    
    for state in range(len(states)):
        for position in range(len(observations)):
            posterior_prob_matrix[state, position] = (forward_matrix[state, position] * backward_matrix[state, position]) / ((forward_prob + backward_prob) / 2)

    return posterior_prob_matrix, forward_matrix, backward_matrix, forward_prob, backward_prob



def baum_welch(states, observations):
    convergence = True #allows us to track if values stop changing

    #creates a dictionary of symbols from the observation sequence and their location within the sequence
    symbols_dict = defaultdict(list)
    for index, symbol in enumerate(observations):
        symbols_dict[symbol].append(index)

    #useful values and matrices to have
    num_states = len(states)
    obs = len(observations)
    posterior_prob_matrix, forward_matrix, backward_matrix, forward_prob, backward_prob = forward_backward_algorithm(states, observations)



    # 3D matrix: from state i to state j position change
    xi = np.zeros((num_states, num_states, obs - 1))

    # denominator = (Pf + Pb) / 2
    denominator = (forward_prob + backward_prob) / 2.0

    # For every position
    for position in range(obs - 1):
        next_obs = observations[position + 1]

        # For every possible state i to state j transition
        for i, state_i in enumerate(states):
            for j, state_j in enumerate(states):

                forward = forward_matrix[i, position] # forward_prob(i, position)
                trans = state_i.trans_probs[state_j.name] # transition_prob(i to j)
                emit = state_j.emission_probs[next_obs] # emission_prob(next_obs given j)
                backward = backward_matrix[j, position + 1] # backward_prob(j, position+1)

                numerator = forward * trans * emit * backward

                xi[i, j, position] = numerator / denominator

    #updates initial probs
    for i, state in enumerate(states):
        new_initial_prob = posterior_prob_matrix[i, 0]
        if abs(new_initial_prob - state.initial_probs) > 0.001:
            convergence = False
        state.initial_probs = new_initial_prob

    #updates emission probs
    row_sums = np.sum(posterior_prob_matrix, axis=1)

    for i, state in enumerate(states):
        for symbol in symbols_dict:
            current_state_posterior = np.array(posterior_prob_matrix[i])
            symbol_prob = np.sum(current_state_posterior[symbols_dict[symbol]])
            new_emission_prob = symbol_prob / row_sums[i]
            if abs(new_emission_prob - state.emission_probs[symbol]) > 0.001:
                convergence = False
            state.emission_probs[symbol] = new_emission_prob
    
    #updates the transition probs
    for i, first_state in enumerate(states):
        for j, second_state in enumerate(states):
            sliced_matrix = xi[i, j, :]
            new_trans_prob = np.sum(sliced_matrix) / (row_sums[i] - posterior_prob_matrix[i, -1])
            if abs(new_trans_prob - first_state.trans_probs[second_state.name]) > 0.001:
                convergence = False
            first_state.trans_probs[second_state.name] = new_trans_prob

    return states, convergence

def main():
    initial_probs = {"I": 0.1, "G": 0.9}
    emission_probs = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}, "G": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4}}
    trans_probs = {"I": {"I": 0.6, "G": 0.4}, "G": {"I": 0.1, "G": 0.9}}
    observations = "ACGCGATC"

    states = create_states(initial_probs, emission_probs, trans_probs)

    
    counter = 0
    convergence = False

    while convergence is False:
        states, convergence = baum_welch(states, observations)
        counter += 1
        print(counter)
        if counter >= 100:
            convergence = True


if __name__ == "__main__":
   main()