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
CALL on function and store in markov_model
PRINT results
```

### Nth order Markov Chain
```

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
