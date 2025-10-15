# Introduction

This project implements the Smith-Waterman algorithm for local sequence alignment. This algorithm finds the most optimal match by building a scoring matrix, and then performing a traceback from the highest scoring node. This gives us the best local alignment between two sequences. 

# Pseudocode

SET UP SCORING SYSTEM
+1 for a match 
-1 for a mismatch 
-1 for a gap 

CREATE SCORING TABLE
Create a matrix with one extra row and one extra column.
The first sequence will run along the top, representing columns.
The second sequence will run down the left, representing rows.
The extra row and column at the top and left start with zeros.

FILL SCORING TABLE
Go through the table one cell at a time, from top-left to bottom-right.
For each cell:
Look at the letters from each sequence that correspond to this row and column.
Check three possible ways to reach this cell, diagonally, from above, from the left.
Then calculate the diagonal score, the up score or the left score.
Take the largest of these three values, but if all of them are negative, replace it with zero.
Record the score in the current cell, making note of direction as well for traceback.
While filling in the table, keep track of which cell has the highest score overall 

TRACEBACK TO BUILD ALIGNMENT
Find cell with the highest score.
Starting from that cell, move backwards through the table following the directions (diagonal, up, or left).
For each move:
If diagonal, it means the two letters were aligned.
If up, it means a letter in the first sequence aligned with a gap in the second sequence.
If left, it means a gap in the first sequence aligned with a letter from the second sequence.
Continue moving until you reach a cell with a score of zero 
(The letters collected during this process form the aligned sequences, but since they were built backwards, reverse them at the end.) 


# Successes
We got much of the program down during our first meeting by going line by line through the instructions provided and writing a pseodocode that reflected what we would be implementing later. We were able to make time to work on the code as a group, and were effective with our time. We did have to do a bit of outside research on a few things, but overall we are pleased with the outcome of our program. 

(Chris)
Planning went really well, and we were able to work through the actual structure of the program/algorithm without too much difficulty.

# Struggles
While we were able to get through much of the program with few issues, we did have some original problems determining which sequence represented columns, and which represented rows within the matrix. We also ran into a problem with getting the aligned sequences to return within `traceback_matrix`. Because they were differing lengths, we could get `seq2` to return, but `seq1` would not due to it being shorter. 

(Chris)
Syntax mistakes are the bane of my existence. I'm too used to working it Visual Studio and having its highlighting to help me identify mistakes. Turns out, if you call something `reversed_aligned_sequence`, you have to keep calling it that and can't suddenly switch to `reverse_aligned_sequence` halfway through. And it's hard to notice that you dropped a 'd'.

# Personal Reflections
## Group Leader - Chris
Solid project, good plan, good implementation. This is the second project where I felt like we nailed the algorithm and outline, then struggled with syntax issues when it came to actually getting the code to work. We got to learn a bit about numpy arrays too, which I haven't worked with before.

## Other member - Abi
Writing this program went fairly smoothly, with a few hiccups, but Chris and I communicated well in our meetings to ensure we covered all things needed for this assignment. We worked through paired programming, which I think worked well, as we could talk through each line of code as we were working on it, and helped one another understand what was happening within the program. 

# Generative AI Appendix
We didn't use gen AI.
