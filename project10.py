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
    seq_prob = 0.0
    first_obs = observations[0]
    for i, state in enumerate(states):
        seq_prob += state.initial_probs * state.emission_probs[first_obs] * backward_probs[i, 0]

    return backward_probs, seq_prob



def forward_backward_algorithm(states, observations):
    '''
    Purpose - Calculate the probability matrix of an observations in a specific state, given the HMM.

    Input -
        states: list of State objects
        observations: string of observations
    Output - Posterior probability matrix, foward and backward matrix, foward and backward probabilies
    '''

    forward_matrix, forward_prob = forward_algorithm(states, observations)
    backward_matrix, backward_prob = backward_algorithm(states, observations)

    posterior_prob_matrix = np.zeros((len(states), len(observations)))
    
    for state in range(len(states)):
        for position in range(len(observations)):
            posterior_prob_matrix[state, position] = (forward_matrix[state, position] * backward_matrix[state, position]) / ((forward_prob + backward_prob) / 2)

    return posterior_prob_matrix, forward_matrix, backward_matrix, forward_prob, backward_prob



def baum_welch(states, observations):
    '''
    Purpose - uses the Baum-Welch Expectation-Maximization approach to improve HMM parameter estimations
    
    Inputs -
        states: list of State objects
        sequences: list of strings of Observations

    Output -
        list of State objects with updated initial, emission, and transition probabilities
        convergence: returns True if the newly calculted probabilites are not significantly different from the previous one
    '''
    convergence = True #allows us to track if values stop changing

    #initializes arrays to hold the calculated averages when using multiple sequences build the model
    num_states = len(states)
    posterior_sums = np.zeros(num_states)
    xi_sums = np.zeros((num_states, num_states))
    emission_sums = {state.name: defaultdict(float) for state in states}
    initial_sums = np.zeros(num_states)

    for observations in sequences:
        #dictionary to hold the index locations of each symbol that appears in the obervation
        symbols_dict = defaultdict(list)
        for index, symbol in enumerate(observations):
            symbols_dict[symbol].append(index)

        #all the matrix and probabilites we need later
        posterior_prob_matrix, forward_matrix, backward_matrix, forward_prob, backward_prob = forward_backward_algorithm(states, observations)

        #builds the xi matrix we need for probability calculations
        xi = np.zeros((num_states, num_states, len(observations) - 1))
        denominator = (forward_prob + backward_prob) / 2.0

        for position in range(len(observations) - 1):
            next_obs = observations[position + 1]
            for i, state_i in enumerate(states):
                for j, state_j in enumerate(states):
                    numerator = forward_matrix[i, position] * state_i.trans_probs[state_j.name] * state_j.emission_probs[next_obs] * backward_matrix[j, position + 1]
                    xi[i, j, position] = numerator / denominator

        initial_sums += posterior_prob_matrix[:, 0]
        posterior_sums += np.sum(posterior_prob_matrix, axis=1)
        for i, state in enumerate(states):
            for symbol in symbols_dict:
                emission_sums[state.name][symbol] += np.sum(posterior_prob_matrix[i, symbols_dict[symbol]])
            xi_sums[i] += np.sum(xi[i], axis=1)

    #updates intitial probabilities 
    for i, state in enumerate(states):
        new_initial_prob = initial_sums[i] / len(sequences)
        if abs(new_initial_prob - state.initial_probs) > 0.001:
            convergence = False
        state.initial_probs = new_initial_prob

        #updates emission probabilities
        for symbol in emission_sums[state.name]:
            new_emission_prob = emission_sums[state.name][symbol] / posterior_sums[i]
            if abs(new_emission_prob - state.emission_probs[symbol]) > 0.001:
                convergence = False
            state.emission_probs[symbol] = new_emission_prob

        #updates transition probabilities
        for j, state_j in enumerate(states):
            new_trans_prob = xi_sums[i, j] / (posterior_sums[i] - initial_sums[i])
            if abs(new_trans_prob - state.trans_probs[state_j.name]) > 0.001:
                convergence = False
            state.trans_probs[state_j.name] = new_trans_prob

    return states, convergence

def main():
    #testing values
    initial_probs = {"I": 0.1, "G": 0.9}
    emission_probs = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}, "G": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4}}
    trans_probs = {"I": {"I": 0.6, "G": 0.4}, "G": {"I": 0.1, "G": 0.9}}
    sequences = ["ACGCGATC", "GCGTAC", "ATCG"] 

    states = create_states(initial_probs, emission_probs, trans_probs) #gives us our list of State objects. 

    
    counter = 0
    convergence = False

    while convergence is False:
        states, convergence = baum_welch(states, observations)
        counter += 1
        print(counter)
        if counter >= 100: #currently crashes at 14 because our probabilites get too small and we aren't in log space
            convergence = True


if __name__ == "__main__":

   main()
