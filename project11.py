import copy as copy
import HMM as HMM
import numpy as np
import ujson as json
from collections import defaultdict
import numpy.random as nr     # Setting up random distributions
import pandas as pd           # Simple convergence checks
from itertools import product # For robust iteration
from array import array       # Faster base Python iteration



def build_profile_from_fasta(fasta_file):
    '''
    Purpose - to open a FASTA file and create a profile array that indicates if a position is a Match or Insertion State.

    Inputs - 
        A FASTA file where all sequences are the same length

    Output -
        column state array, the length of the sequences in the FASTA file where each position is the state of the column (Numpy array)
        total sequence array, where each row is a sequence and each column position is a position in the sequence. (Numpy array)
    '''
    sequences = []

    with open(fasta_file) as file:
        for line in file:
            line = line.strip()
            # Ignore headers
            if line.startswith(">"):
                continue

            # Check that all sequences are same length
            seq_length = None
            if seq_length is None:
                seq_length = len(line)
            elif len(line) != seq_length:
                raise ValueError("Sequences are differing lengths.")

            # Convert line into array and store it
            seq_array = np.array(list(line))
            sequences.append(seq_array)

    # Stack rows into final 2D numpy matrix
    total_sequence_array = np.vstack(sequences)

    num_sequences = total_sequence_array.shape[0]
    column_state_array = np.empty(seq_length, dtype=object)

    counter = 0
    for col in range(seq_length):
        column = total_sequence_array[:, col]

        gap_count = np.sum(column == "-")
        residue_count = num_sequences - gap_count

        # Match state if fewer than half the column are gaps, otherwise insertion
        half_sequences = num_sequences / 2

        if gap_count >= half_sequences:
            state_label = "I"   # Insertion
        else:
            state_label = "M"   # Match
            counter += 1

        column_state_array[col] = state_label + str(counter)

    return column_state_array, total_sequence_array



def generate_labeled_residue_array(total_sequence_array, column_state_array):
    '''
    Purpose - Creates a matrix that is the same size as the total_sequence_array, where each position is the state
            of the residue in the same position in the total_sequence_array

    Input - 
        column_state_array, the length of the sequences in the FASTA file where each position is the state of the column (Numpy array)
        total_sequence_array, where each row is a sequence and each column position is a position in the sequence. (Numpy array)

    Output - 
        labeled_residue_array, a matrix the same size as the total_sequence_array, which holds the state 
                            assigned to the residue in the same location in the total_sequence_array
    '''
    labeled_residue_array = np.empty_like(total_sequence_array, dtype="U2")
    for row in range(len(total_sequence_array[:,0])):
        counter = 1
        for column, state in enumerate(column_state_array):
            if state[0] == "M" and total_sequence_array[row, column] != "-":
                labeled_residue_array[row, column] = "M" + str(counter)
                counter += 1
            elif column_state_array[column][0] == "M" and total_sequence_array[row, column] == "-":
                labeled_residue_array[row, column] = "D" + str(counter)
                counter += 1
            elif column_state_array[column][0] == "I" and total_sequence_array[row, column] != "-":
                labeled_residue_array[row, column] = "I" + str(counter - 1)
            elif column_state_array[column][0] == "I" and total_sequence_array[row, column] == "-":
                labeled_residue_array[row, column] = "--"
    return labeled_residue_array


def generate_states_and_transitions(labeled_residue_array):
    '''
    Purpose - Generates the list hidden states and initializes the trans_probs and intitial_probs dicts to store all possible transitions for the pHMM
    
    Input - 
        labeled_residue_array, a matrix the same size as the total_sequence_array, which holds the state 
                            assigned to the residue in the same location in the total_sequence_array
    
    Output -
        hiddenstate - a list of all possible states in the pHMM
        trans_probs - a dict of dict of floats to hold the probabilities of all possible state transitions in the model
        initial_probs - a dict of floats to hold the initital state probabilites of the model
    '''
    hiddenstates = []
    pHMM_length = int(labeled_residue_array[-1, -1][1])
    for position in range(pHMM_length + 1):
        hiddenstates.append("M" + str(position))
    for position in range(pHMM_length + 1):
        hiddenstates.append("I" + str(position))
    for position in range(1, pHMM_length + 1):
        hiddenstates.append("D" + str(position))
    hiddenstates.append("M" + str(pHMM_length + 1))

    trans_probs = defaultdict()
    for state in hiddenstates[:-1]:
        position = int(state[1])
        possible_trans = {"M" + str(position + 1): 0, "I" + str(position): 0, "D" + str(position + 1): 0}
        if ("D" + str(pHMM_length + 1)) in possible_trans:
            del possible_trans["D" + str(pHMM_length + 1)]
        trans_probs[state] = possible_trans


    initial_probs = defaultdict()
    for state in hiddenstates:
        initial_probs[state] = 0
    initial_probs[hiddenstates[0]] = 1

    return hiddenstates, trans_probs, initial_probs



def compute_emission_probabilities(column_state_array, total_sequence_array):
        '''
        Purpose - calculates the emission probabilities based on our initial sequences and states

        Input -
            column state array, the length of the sequences in the FASTA file where each position is the state of the column (Numpy array)
            total sequence array, where each row is a sequence and each column position is a position in the sequence. (Numpy array)
        
        Output -
            emission_probs, a dict of dict of floats that contains the emission probabilities for states that have emissions
        '''
        emission_probs = {}
        insertion_residue_counts = {}

        # Count all residues
        for sequence in total_sequence_array:
            for residue in sequence:
                if residue != "-":
                    insertion_residue_counts[residue] = insertion_residue_counts.get(residue, 0) + 1

        # Compute insertion emission probabilities
        insertion_denominator = sum(insertion_residue_counts.values()) + 20
        insertion_emissions = {
            residue: (count + 1) / insertion_denominator
            for residue, count in insertion_residue_counts.items()
        }

        for state in column_state_array:

            emission_probs[state] = {}

            # Match state
            if state.startswith("M"):
                # Extract index of match column
                column_index = int(state[1:]) - 1

                # Get column values
                column_residues = total_sequence_array[:, column_index]
                match_counts = {}

                for residue in column_residues:
                    if residue != "-":
                        match_counts[residue] = match_counts.get(residue, 0) + 1

                # Apply pseudocount
                match_denominator = sum(match_counts.values()) + 20

                for residue, count in match_counts.items():
                    emission_probs[state][residue] = (count + 1) / match_denominator

            # Insertion
            elif state.startswith("I"):
                # Use insertion emissions
                emission_probs[state] = insertion_emissions.copy()

        return emission_probs



def compute_transition_probabilities(trans_probs, labeled_residue_array):
    '''
    Purpose - calculates the transition probabilities from all observed transitions

    Input - 
        labeled_residue_array, a matrix the same size as the total_sequence_array, which holds the state 
                            assigned to the residue in the same location in the total_sequence_array
        trans_probs, a dict of dict of floats to hold the probabilities of all possible state transitions in the model
    
    Output -
        trans_probs, a dict of dict of floats that now holds the probabilities of all possible state transitions in the model
        observed_transitions, a dict of dict of ints that holds the counts for each observed transition from one (outer) state to another (inner) state
    '''
    observed_transitions = copy.deepcopy(trans_probs)

    #gets M0 start state transitions
    for row in labeled_residue_array[:, 0]:
        next_state = row
        observed_transitions["M0"][next_state] = observed_transitions["M0"].get(next_state, 0) + 1

    #gets counts for other state transitions, except to end state
    for row in labeled_residue_array:
        for position in range(len(row) - 1):
            start_state = row[position]
            if start_state != "--":
                next_position = position + 1
                next_state = row[next_position]
                while next_state == "--":
                    next_position += 1
                    next_state = row[next_position]
            
                observed_transitions[start_state][next_state] = observed_transitions[start_state].get(next_state, 0) + 1

    #gets counts for transitions to the end state
    for row in labeled_residue_array[:, -1]:
        start_state = row
        end_state = int(start_state[1:]) + 1
        observed_transitions[start_state]["M" + str(end_state)] += 1

    
    #Calculating transition probs from the counts in observed_transitions
    for start_state in trans_probs:
        denominator = sum(observed_transitions[start_state].values()) + len(trans_probs[start_state].keys()) #pseudocount of 1 for each transition
        for transition in trans_probs[start_state]:
            trans_probs[start_state][transition] = (observed_transitions[start_state][transition] + 1) / denominator

    return observed_transitions, trans_probs



#FORWARD
def forward_sequence(sequence, model):
    forward_prob = model.forward(sequence)
    log_prob = np.log10(forward_prob)
    return forward_prob, log_prob


#VITERBI
def viterbi_sequence(sequence, model):
    return model.viterbi(sequence)


def main():

    fasta_file = "phmm_train_motif1.fasta"

    alphabet = "ARNDCEQGHILKMFPSTWYV"
    column_state_array, total_sequence_array = build_profile_from_fasta(fasta_file)
    labeled_residue_array = generate_labeled_residue_array(total_sequence_array, column_state_array)
    hiddenstates, trans_probs, initial_probs = generate_states_and_transitions(labeled_residue_array)
    observed_transitions, trans_probs = compute_transition_probabilities(trans_probs, labeled_residue_array)
    emission_probs = compute_emission_probabilities(column_state_array, total_sequence_array)

    test_sequence = "VGQDH"

    pHMM = HMM.HMM(alphabet=alphabet, hidden_states=hiddenstates, init_probs=initial_probs, trans_probs=trans_probs, emit_probs=emission_probs)
    print(pHMM)

    #print(total_sequence_array)
    #print(column_state_array)
    #print(labeled_residue_array[0, 0])
    #print(hiddenstates)
    #print(trans_probs)
    #print(initial_probs)
    #print(observed_transitions)
    #prob, logprob = forward_sequence(test_sequence, pHMM)
    #viterbi_path = viterbi_sequence(test_sequence, pHMM)
    #print(logprob, viterbi_path)

if __name__ == "__main__":
    main()