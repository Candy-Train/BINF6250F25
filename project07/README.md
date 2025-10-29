# BINF6250F25
Project 07
Christopher Fitzgerald, Tiange Feng
# Introduction
This assignment covers the complete implementation of the Burrows-Wheeler Transform (BWT) pipeline, from construction to application. We implemented the BWT algorithm, exploring both the naive rotational sorting method and the more efficient approach using a pre-computed suffix array. Following this, the focus shifted to pattern matching by building the FM-Index. This involves constructing the necessary auxiliary data structures—specifically the count and occurrence arrays. Finally, we applied these structures to implement the full BWT-based search algorithm, enabling the efficient location of all exact matches of a query string within a reference text.

# Pseudocode
Pseudocode and planning goes here

## BWT
```
add the '$' to the end of the string
Initialize the bwt list for holding the rotations
Interate through the string and perform the rotations by attaching the first portion of the string to the last portions (str[i:] + str[:i])
Sort the bwt list lexicographically
Assemble the transformed string from the last character of the sorted rotated strings
```
## Suffix Array

```
Add the '$' to the end of the string
Initializse a list for suffix position
Iterate through the string, taking each suffix (string[i:]) and creating a tuple of the suffix and its position
Add the tuple to the suffix position list
Sort the list lexicographically
Create and fill a list for the suffix array by interating through the sorted list and taking the position (suffix_pair[1]) from each suffix_pair tuple
```

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
```
Use the count and occurance arrays to update the range
If the lower range is 0, then the new range is the count[char] + 0 + 1
Else, the lower range is the count[char] + occurance[char][lower - 1] + 1
The new upper range is count[char] + occurance[char][upper] - 1
```
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

# Successes
We successfully completed this assignment, and the overall logic and process were quite straightforward.

# Struggles
The only real struggle we had was when we tried to join some code we had worked on separately. I (Chris) had a function for update_range that worked when I ran it on it's own, but not when we integrated it into the rest of the program. Tiange rewrote it, and her version worked, but we didn't see a difference between the two functions. So we never really figured out why my version had a problem. 

# Personal Reflections
## Group Leader (Chris)
This felt pretty smooth. We both felt like we understood the algorithm pretty well, and were able to get through a pseudocode plan fairly easily. We broke off, wrote some functions separately, then joined them all together. It went mostly without issue.

## Other member - Tiange
Our collaboration went very well. In our first meeting, we clarified the relationships between all the functions, completed a portion of the pseudocode and initial coding, and then individually finished the remaining parts. The only issue we encountered was an initial mismatch with the list indexing and variables between the update_range function and the occurrence array. However, we quickly located the source of the problem and resolved it.

# Generative AI Appendix
We didn't use any AI.
