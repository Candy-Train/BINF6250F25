# Introduction
Description of the project
This project focuses on graph theory, specifically the Graph Algorithm Shortest Path. This module honed in what graphs exhibit and all their data points convey. An added detail was Eulerian walks in graphs with nodes and edges of a graph to gather detail between data points and their distance.
 
# Pseudocode

1. **Graph Construction**: Create nodes for all (k-1)-mers from the set of k-mers in the sequencing reads.

  Cut out each kmer
  left kmer is kmer-last character
  right kmer is kmer-first character

  compare all but the first character of the left kmer to all but the last character of the right kmer
  if these middle characters are the same, there is overlap between the nodes, and we use 'add_edge'
  
  stop when we get to length of the string - (k - 1)


2. **Path Finding**: Find an Eulerian path through the graph, which represents a possible reconstruction of the original sequence.

   using the 'first_node' as our starting position, make a list of possible next steps from the list of values for the current node in our graph
   take a step to one of those nodes
   use 'remove_edge' to remove that edge from our graph
   repeat, using the current node as our new starting postion
   continue until there are no more possible steps



# Successes
I feel like we had a solid understanding of the algorithm we needed to construct, and what each piece of it needed to do. Our plan was clear and easy to follow when we started coding.
 
# Struggles
A few small syntax errors had caused issues, but the team tried attacking the issue from multiple points at the instruction of the team leader and was able to pinpoint the exact hang up.


These syntax errors actually consumed most of our time on this project. I think it comes back down to knowing that Python *can* do something, but not understanding how to integrate it properly. 
 
 
# Personal Reflections
## Group Leader
This felt like one of the smoothest assignments so far. We talked through a plan, then executed it. If it wasnt for the syntax error we ran into, we would have been done after our first pass through. Usually, the plan requires modification once we start coding because there's something with the algorithm we overlooked.
 
## Other member
Other members' reflections on the project
I really found the idea of this project very interesting. I never looked at graphs in the way this module set it up to. I also had to go back to a prior course lecture notes on Classes and their set up. It is not easy to grasp the idea of it, but practice building simple classes and my team's knowledge on it, helped a lot.
 
# Generative AI Appendix
We did not use any generative AI.
