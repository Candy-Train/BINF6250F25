import numpy as np
import math

class State:
    def __init__(self, initial_probs, emission_probs, trans_probs, name):
        self.initial_probs = initial_probs
        self.emission_probs = emission_probs
        self.trans_probs = trans_probs
        self.name = name

def calc_max(states, max_previous, current, observations):

    #Recursion equation (i=1...L): vl(i) = el(xi) * maxk(vk(i–1)akl)

    maximum = []

    for i in range(len(max_previous)):
        state = states[i].name
        maximum.append(math.log2(current.emission_probs[observations]) + (math.log2(current.trans_probs[state]) + max_previous[i]))
        
    max_index = np.argmax(maximum)

    return max(maximum), max_index


def build_probability_matrix(states, observations):

    probability_matrix = np.zeros((len(states), len(observations)))
    traceback_matrix = np.zeros((len(states), len(observations)), dtype=int)

    initialization = observations[0]
    for i, state in enumerate(states):
        probability_matrix[i, 0] = math.log2(state.initial_probs) + math.log2(state.emission_probs[initialization])
        traceback_matrix[i, 0] = 0
    
    # recursion
    for j in range(1, len(observations)):
        current_obs = observations[j]

        for i, current_state in enumerate(states):
            previous = probability_matrix[:, j - 1]
            max, max_index = calc_max(states, previous, current_state, current_obs)
            probability_matrix[i, j] = max
            traceback_matrix[i, j] = max_index
    
    return probability_matrix, traceback_matrix


def traceback(traceback_matrix, observations, final_state_index, state_names):
    """
    Constructs the most probable path through states.

    Inputs:
        traceback_matrix: 2D array of ints
        observations: string/list of observations
        final_state_index: index of final best state (int)
        state_names: list of state names (for labeling the output path)

    Output:
        path (list of strings): most likely sequence of state names
    """
    num_obs = len(observations)
    # number of characters in the observation string
    path = [None] * num_obs
    # initializes path which will be repeated through the length of the observations string, and then assigned a position
    path[-1] = state_names[final_state_index]
    # sets the last entry of the path to the name corresponding with the final state index

    # Backtrack through traceback matrix
    for j in range(num_obs - 1, 0, -1):
        prev_index = traceback_matrix[final_state_index][j]
        # looks up stored index of prior state name for the current state index in the column
        final_state_index = prev_index
        # updates final state index to the prior state index for the next iteration
        path[j - 1] = state_names[final_state_index]
        # stores the state name corresponding with the prior state index into the position at j - 1

    return path
    # returns full list of state names


def create_states(initial_probs: dict, emission_probs, trans_probs):
    '''
    Purpose - Create all State objects

    Inputs -
        initial probabilities (dict)
        emission probabilities (dict of floats)
        transition probabilities (dict of floats)
    Output -
        a State (object)
    '''
    states = []

    for key in initial_probs.keys():
        key = State(initial_probs[key], emission_probs[key], trans_probs[key], key)
        states.append(key)
    
    return states

def main():
    initial_probs = {"I": 0.1, "G": 0.9}
    emission_probs = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}, "G": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4}}
    trans_probs = {"I": {"I": 0.6, "G": 0.4}, "G": {"I": 0.1, "G": 0.9}}
    states = create_states(initial_probs, emission_probs, trans_probs)
    observations = "ACGCGATC"

    state_names = []
    for state in states:
        state_names.append(state.name)

    probability_matrix, traceback_matrix  = build_probability_matrix(states, observations)

    trace = traceback(traceback_matrix, observations, 1, state_names)
    print(probability_matrix)
    print(traceback_matrix)
    print(trace)

if __name__ == "__main__":
   main()