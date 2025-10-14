# Introduction
Description of the project

# Pseudocode

```
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
