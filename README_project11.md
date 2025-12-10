# Introduction
Profile Hidden Markov Models are a tool used in understanding protein structures and function, by identifying sequence similarities. They show the evolutionary chaanges 
that have occurred in related sequences, and provide information about amino acid conservation throughout position/ time. Importantly, pHMMs show where and when insertions and 
deletions occurred, which have real world implications in biological research.

# Pseudocode
```
## Function 

Purpose - to open a FASTA file and create a profile array the indicates if a position is a Match or Insertion State.

Inputs - 
	A FASTA file where all sequences are the same length

Output -
	A `column state array`, the length of the sequences in the FASTA file (Numpy array)
	A `total sequence array`, where each row is a sequence and each column position is a position in the sequence. (Numpy array)

Open the FASTA file
For each line
	If the line starts with ">", pass
	for the each  sequence
		Verify the sequence is the same length as previous sequences
			could throw an error if it isn't the same length.
		Create an array that is the length of the sequence and fill the array with the residues.
		Stack the array to a `total sequence array`

get the the number of rows in the array (the length of a column)

For each column
	Count the number of "-" (gaps) in the column
	The number of residues is the length of the column minus the number of gaps
	Create a new array that is the length of the sequences
	Fill each position in the array with either Match State(i), if fewer than half of the values in the same position in the total sequence array are a gap, or Insertion State(i) if at least half of the values are a gap.



## Function 2

Create an array that is the same size as the `total sequence array` (`labeled residue array`)

For each position in the `column state array`
	check the same position in each sequence (`total sequence array`)
	If the column is Match, and the sequence has a residue -> fill in the matching location in the labeled residue array with M(i)
	If the column is Match, and the sequence doesnt have a residue -> fill in the matching location in the labeled residue array with D(i)
	If the column is Insertion, and the sequence has as residue -> fill in the matching location in the labeled residue array with I(i)
	If the column is Insertion, and the sequence doesnt have a residue -> fill in the matching location in the labeled residue array with `NaN`

## Function 3
Set up the pHMM

Create a list of all possible States (`hiddenstates`)
	start state - M0
	all Match states - M1-ML
	all Insertion state - I0-IL
	all Deletion states - D1-DL
	end state - ML+1
	L should be equal to the length of the pHMM, which is the highest Match state from the `labeled residue array`(M3 in our short training file)

set up possible transitions
For each state in `hiddenstates`
	create a dict where each key is a state from `hiddenstates`, except for the end state
	for each key, the value is a dict where each key is each possible transition and the values are the probabilities (not yet calculated)
	inner dict keys can be determined from the name of the outer dict key. The second character in the out dict key name is the positions (0-L). We can use that character (i), convert it to an `int` and increment it for the names of the inner dict key. Mi can transition to Ii, Mi+1, Di+1. This creates the dict of dict of floats for `trans_probs`



## Function 4
Parameter estimation

#### Transition probabilities
example `observed_trans` -> M0[M1: '', I0: '', D1: '']

For each outer key in `trans_probs`
	get a list of the inner keys (observed transitions)
	search the `labeled residue array` to collect a count of each observed transition and store them as a dict (`observed_trans`) where the key is the observed transition state and the value is the count
	If all counts are 0, set the count of M(i) to number of sequences (length of column or number of rows). This is to account for reaching the end state, where no further transitions occur.
	Fill in the probabilities for `trans_probs`
	the denominator for the equation is the sum of `observed_trans` + 3
	For inner key in `trans_probs`
	trans_probs(outer key)(inner key) = observed_trans(inner key) + 1 / denominator

#### Emission probabilities

Create an `emission_probs` dict where the keys are the `hiddenstates`, except for the start and end states.

Insertion Emission Values
Create a dict where the keys are all the residues from the `total sequence array` and the values are their counts
Create a dict (`inner insertion emission probs`) where the keys are all the observed residues from the sequences (same keys as previous dict) and the values are equal to residue_count(key) + 1 / sum(residue_count) + 20

For each key in `emission_probs`
	If the key starts with 'M'
		Get the index location of the matching states in the `labeled residue array`
		From the same locations in the `total sequence array`, get the residues and their counts as a dict (`residue_count`) where the key is the residue and the value is its count. 
		The keys from this dict will also be the keys for the inner dict of our `emission_probs`.
		The values for the inner dict are equal to residue_count(inner key) + 1 / sum(residue_count) + 20
	If the key starts with 'I'
		fill in the Insertion Emission values
```

# Successes
Once we grasped what we were going to be accomplishing with creating a profile HMM, the majority of the programming was easy. We were able to complete most of the required new
functions with very few issues, and we understood the process of what we were doing. 

Note: We found an outside resource that was very helpful in our understanding if you are interested in checking it out. 
https://www.cs.cmu.edu/~durand/03-711/2010/Lectures/hmm10-5.pdf

# Struggles
We had a bit of trouble starting out, just getting our wits about us to understand fully what we were supposed to be doing. It was a little overwhelming having as much 
information as we did, and also trying to learn the code provided to us. We did have a bit of trouble with the transition probabilities not pulling the correct counts, 
which was easy enough to fix, we just had to do it in a less elegant way. We also ran into some serious issues integrating our code with Marcus's program, though we tailored 
everything to be easy to integrate. We were not able to complete doing the forward probabilities and Viterbi path due to these integration problems. We also ran into some problems
with understanding how to handle the emmission probabilities of states that don't emit (start, deletion and end).

# Personal Reflections
## Group Leader - Chris
Group leader's reflection on the project

## Other member - Abi
This project was a tough one to end on. I figured it would be tricky, especially with trying to tailor our functions to integrate with the code given to us, but it was a bit more
frustrating than I imagined. We wrote our functions with very few issues, but when we tried to integrate everything, it seemed to all fall apart, despite our efforts to make it 
all mesh well. We did not fully complete the project, which was a defeating note to end on, and I wish that we had been given more time to work on it.

# Generative AI Appendix
As per the syllabus
