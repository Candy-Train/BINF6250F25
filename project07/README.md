# BINF6250F25
Project 07
Christopher Fitzgerald, Tiange Feng
# Introduction
This assignment covers the complete implementation of the Burrows-Wheeler Transform (BWT) pipeline, from construction to application. We implemented the BWT algorithm, exploring both the naive rotational sorting method and the more efficient approach using a pre-computed suffix array. Following this, the focus shifted to pattern matching by building the FM-Index. This involves constructing the necessary auxiliary data structures—specifically the count and occurrence arrays. Finally, we applied these structures to implement the full BWT-based search algorithm, enabling the efficient location of all exact matches of a query string within a reference text.

# Pseudocode
Pseudocode and planning goes here

## find_match
```
function find_match(pattern,transformed,counts,occurrences,suffix positions)
  Initialize search range to cover the entire transformed text
  for each character in the pattern, processing from right to left do
    Update the search range based on the current character
    if the range becomes empty then
      return empty list as pattern is not found
  Collect all suffix positions within the final range
  return the list of matching positions
```

## BWT

## Suffix Array

## Count Array
```
function calculate_counts(transformed,alphabet)
  Initialize a dictionary to track character counts
  Initialize a result dictionary for cumulative counts
  Set initial cumulative count to zero
  for each character in the sorted alphabet do
    Store the current cumulative count for this character
    Increase the cumulative count by the frequency of this character
  return the dictionary of cumulative counts
```

## Occurrence Array
```
function calculate_occurrences(transformed,alphabet)
  Initialize a dictionary mapping each character to an array of zeros
  for each position in the transformed text do
    Identify the character at the current position
    for each character in the alphabet do
      Copy the previous occurrence count to the current position
    Increment the occurrence count for the current character
  return the dictionary of occurrence counts
```

## update_range

# Successes
We successfully completed this assignment, and the overall logic and process were quite straightforward.

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member - Tiange
Our collaboration went very well. In our first meeting, we clarified the relationships between all the functions, completed a portion of the pseudocode and initial coding, and then individually finished the remaining parts. The only issue we encountered was an initial mismatch with the list indexing and variables between the update_range function and the occurrence array. However, we quickly located the source of the problem and resolved it.

# Generative AI Appendix
As per the syllabus
