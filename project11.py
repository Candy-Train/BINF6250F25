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



def compute_emission_probabilities(column_state_array, total_sequence_array):
        
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

    

def generate_labeled_residue_array(total_sequence_array, column_state_array):
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
    Docstring for function_3
    
    :param labeled_residue_array: Description
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

    return hiddenstates, trans_probs, initial_probs



def estimate_parameters(trans_probs, labeled_residue_array):
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
    model.hidden_states.pop(0)
    forward_prob = model.forward(sequence)
    log_prob = np.log10(forward_prob)
    return forward_prob, log_prob

#VITERBI
def viterbi_sequence(sequence, model):
    return model.viterbi(sequence)

column_state_array, total_sequence_array = build_profile_from_fasta("phmm_train_motif1.fasta")
labeled_residue_array = generate_labeled_residue_array(total_sequence_array, column_state_array)
hiddenstates, trans_probs, initial_probs = generate_states_and_transitions(labeled_residue_array)
observed_transitions, trans_probs = estimate_parameters(trans_probs, labeled_residue_array)
emission_probs = compute_emission_probabilities(column_state_array, total_sequence_array)


for initial_state in trans_probs["M0"]:
    initial_probs[initial_state] = trans_probs["M0"][initial_state]

test_sequence = "VGQDH"








#print(total_sequence_array)
#print(column_state_array)
#print(labeled_residue_array[0, 0])
#print(hiddenstates)
#print(trans_probs)
#print(observed_transitions)
pHMM = HMM.HMM(alphabet="ARNDCEQGHILKMFPSTWYV", hidden_states=hiddenstates, init_probs=initial_probs, trans_probs=trans_probs, emit_probs=emission_probs)
print(pHMM)
#prob, logprob = forward_sequence(test_sequence, pHMM)
#viterbi_path = viterbi_sequence(test_sequence, pHMM)
#print(logprob, viterbi_path)