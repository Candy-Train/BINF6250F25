# BINF6250F25
# Introduction
Description of the project

# Pseudocode
```
FUNCTION read_fasta

Open the FASTA file for reading.
Create an empty dictionary to store sequences.
Initialize variables to keep track of the current sequence ID and its sequence string.
Read the file line by line:
If the line starts with the ‘>’:
If there is already a current sequence being read, store it in the dictionary with its ID as the key.
Extract the new sequence ID from the line.
Start a new empty sequence string for this ID.
Otherwise:
Remove any extra whitespace.
Add the line’s sequence content to the current sequence string.
After the loop finishes, make sure the last sequence is stored in the dictionary.
Return the dictionary of all sequence IDs and their sequences.

FUNCTION cal_score

Compare the two characters at the current position in each sequence:
If they match, calculate a “diagonal” score by adding the match reward to the score diagonally above-left in the matrix.
If they do not match, calculate a diagonal score using the mismatch penalty.
Calculate the “up” score by adding a gap penalty to the score directly above.
Calculate the “left” score by adding a gap penalty to the score directly to the left.
Choose the maximum among the various scores.
Return this maximum as the score for the current cell in the scoring matrix.

FUNCTION smith_waterman

Determine the number of rows and columns needed for the scoring matrix based on the lengths of the two sequences.
Create a matrix of zeros of that size.
Initialize the maximum score to zero.
For each cell in the matrix (ignoring the first row and column):
Use the scoring function described above to calculate the best possible score for that cell.
Store that score in the matrix.
If the score is greater than the current maximum, update the maximum score.
When the entire matrix is filled, compute a normalized score:
Divide the maximum score by the theoretical maximum possible score (based on sequence lengths and match reward).
Return the normalized similarity score.

FUNCTION build_distance_matrix

Collect all sequence IDs into a list.
Create an empty square matrix with one row and column for each sequence.
For each pair of sequences:
Compute their Smith-Waterman similarity score.
Convert this to a distance value by subtracting the similarity from 1.
Store this distance value in the matrix.
Return both the distance matrix and the list of sequence IDs.

FUNCTION get_min_distance

Initialize a variable to track the smallest distance found and its position.
Loop through every cell in the distance matrix:
Skip diagonal entries.
If the current value is smaller than the stored minimum, update the minimum value and record its coordinates.
Return the position of the closest pair and their distance.

CLASS Node

Each node contains:
A name (the sequence ID or cluster name)
A list of child nodes
A reference to its parent
A branch length (distance from its parent)
When adding a child node:
Store the child inside the parent’s list of children.
Set the parent reference inside the child.
Record the branch length.


FUNCTION neighbor_joining

Using the distance matrix and list of sequence labels, repeat the following process until all sequences are joined:
Compute the divergence for each sequence, which is the sum of its distances to all others.
Create an adjusted distance matrix by adjusting for divergence using the Neighbor-Joining formula.
Find the pair of nodes (i, j) with the smallest adjusted distance.
Compute the branch lengths for each node based on the distances and divergence values.
Create new node objects for the two sequences being joined, including their branch lengths.
Create a new label representing the merged cluster in Newick format.
Remove the two old sequences from the label list and distance matrix.
Compute distances from the new merged node to all remaining nodes.
Insert this new node as a replacement in the matrix and label list.
Once all sequences are merged, return the final distance matrix and the list of labels (the last label is the full Newick tree string).

FUNCTION plot_tree

Take the final output from the Neighbor-Joining step (the distance matrix and labels).
Extract the last label
Append a semicolon to the end of the string.
Use a tree visualization library to:
Parse the Newick string into a tree structure.
Set visual options.
Render the tree on screen or inline in a notebook.

FUNCTION __main__

Read the HIV RT sequences from the provided FASTA file.
Build a distance matrix using the Smith-Waterman algorithm for all pairwise comparisons.
Apply the Neighbor-Joining algorithm to construct the phylogenetic tree.
Print the resulting Newick tree string.
Plot the tree.
```
# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
