# Introduction

The goal of this project is to build a Markov model from words and implement it to generate new texts. The texts we will use for this project include Dr. Seuss' *One Fish Two Fish* and William Shakespeare's *Sonnet 1*.

# Pseudocode

### Train Markov model

```   
FUNCTION build_markov_model(markov_model = dict, new_text = str):
  words <- split new_text using .split() and store words in a list 
  key <- loop through words and store unique words is a listt
  
  
  start_dict <- dictionary for start words 
  store first word in words list in start_dict and set value to 1 
  markov_model['*S*'] <- start_dict
  
  
  FOR each unique word in key count frequency of words that occur after
    inner_dict <- inner dictionary with frequency counts
    indices <- indices of each word found using enumerate()
    
    FOR each position in indices
      IF the position is not the last index
        next_word <- word in the index after position
        
        IF the next_word is not already in inner_dict
          set next_word as a new key with value of 1
        ELSE
          add 1 to the existing key
      
      ELSE 
        create *E* key and set as 1
    
    SET the unique words as the key for markov_model and use the inner_dict as the values
    
  RETURN markov_model
  
INITIATE markov_model dictionary
text <- string 
CALL on build_markov_model using markov_model and text and UPDATE results in markov_model
PRINT markov_model

    
```

### Nth order Markov Chain
```
FUNCTION build_markov_model(markov_model = dict, text = str, order = int w/ default of 1)
  ADD end state to text
  SPLIT text to create list

  GET the first few words based on order to get start state
  INITIATE inner dictionary for start state
  SET inner dictionary for start state as 1
  ADD start state dictionary to the start state key of the markov_model

  FOR each position for the text to text-order(the last position of the combo)
    current_combo <- tuple of the text
    next_text <- word after the combo

    IF the combo is not in the markov_model
      CREATE key for markov_model where the combo is the key

    IF next_text is a value in the combo of the markov_model
      UPDATE inner key by 1
    ELSE
      CREATE new key for the combo of the markov_model and set as 1

  IF the order is 1
    RETURN markov_model
  ELSE
    SET the order to order-1
    CALL on this function
    RETURN markov_model

INITIATE markov_model dictionary
text <- string 
CALL on build_markov_model using markov_model, text, and nth order and UPDATE results in markov_model
PRINT markov_model
```

### Generate text from Markov Model
```
USE numpy

FUNCTION get_next_word(current_word = tuple, markov_model = dict of dict, seed)
  SEARCH outer key of markov_model and save inner key to a new dictionary
  CALCULATE the total values of the dictionary
  
  FOR each key of the dictionary
    CALCULATE and update the probability of each word 
    
  words <- SAVE list of keys  
  probabilities <- SAVE list of values  
  
  USE np.random.choice(words, probabilities) to select next_word randomly
  SELECT next_word using random number generator 

  
  RETURN next_word
  

FUNCTION generate_random_text(markov_model = dict of dict, seed)
  sentence <- CALL on get_next_word to using start state and markov model to get first word
  
  SET current_word to start_state
  WHILE current_word != '*E*'
    current_word <- CALL on get_next_word using current_word and markov_model to update the current_word
    APPEND current_word to sentence
  
  REMOVE the end state from the sentence
  
  RETURN sentence
```
### All the Fish
```
INITIATE markov_model dictionary

READ text 
  FOR each line
    markov_model <- CALL on build_markov_model using markov_model, line, and order to update markov_model dictionary

CALL and print the results from generate_random_text using markov_model
    
```

### Shakespeare
```
INITIATE sonet_markov_model dictionary
OPEN sonnets.txt file
INITIATE empty sonnet line

FOR each line in the file
  line <- REMOVE white spaces
    IF line is empty
      CALL on build_markov_model using sonnet_markov_model and the sonet
    ELSE
      ADD line to the current sonnet 

CALL and print the results from generate_random_text using sonet_markov_model
```


# Successes

* We were able to build the first order markov_model
* We used the first order markov_model to test the `generate_next_word` and `generate_random_text` functions, which we were able to successfully program
  * We saved the inner dictionary of the a separate dictionary to calculate and update the values with the probabilities before using the `np.random.choice()` function. 

# Struggles

* First order `build_markov_model()` function - we struggled with getting all next_words. Our loop initially looped through the text by comparing the targeted word and the word in the text. If the words are the same, the code would find index of the word using `find()` and get the next word. However, this method caused our program to get stuck on the first `fish` found and improperly iterate through the text to find all next words. We later used `enumerate()` to find all indices before looping based on the positions instead. 

* Nth order markov chain - we struggled to correctly implement recursion so that it would correctly build the markov model. 

* `generate_next_word()` function - we needed to learn how to use and implement the `np.random.choice()` function.
* `generate_new_text()` function - we struggled to update our function to account for the Nth order markov chain.



# Personal Reflections

## Group Leader

Group leader's reflection on the project

## Other members

### Zoe Chow
This project was a greater challenge than the previous assignment. While I understood the conceptual requirements for implementing a first-order Markov chain, creating the nested dictionary structure was more complex. Having not programmed in Python for some time, I needed to refresh my understanding of dictionary operations and nested data structures. I reviewed my notes on dictionaries from BINF6200 to remind myself of the methods of implementing nested dictionaries. Despite properly getting the desired Markov model, I believe there are simpler and more straight forward methods to build a dictionary of dictionaries than the one we used. 

The nth order Markov chain implementation was much more challenging. Without prior experience with recursive programming, I struggled to conceptualize how the function would call itself to build complex n-gram patterns. I will need to continue to read about and practice recursions before I am fully comfortable with the concept. 

In contrast, I felt confident implementing the `generate_next_word()` and `generate_new_text()` functions. The logic behind the functions was relatively straightforward. However, our group had no prior experience with the function `np.random.choice()`. Thankfully, the function was easy to learn and we modified our code appropriately to properly implement this function. 


### Little Butler

# Generative AI Appendix

As per the syllabus
