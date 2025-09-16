# Introduction
For this project, our goal is to open a VCF (Variant Call Format) file and parse the data within so that we can provide a dictionary of disease names that have allele frequencies < 0.0001, and the number of occurrences of those diseases in the data set.

# Pseudocode
### Functions
These are the functions we will need in order to complete the project

`read_file`
	takes the file path as a `str`
	opens the file from that path
	create an empty `dictionary` to be used by `disease_counter`
	iterate through the lines
	pass each line to `parse_line`
	take the result from `parse_line` and store it in a dictionary
	Dictionary key:value pair is the name of the disease and the number of times we have seen in from `parse_line`


`parse_line`
	takes a `str` as an argument. That `str` should be a single line from the file, passed to it by `read_file`
	We only care about the 8th "column", which is INFO, and the line is tab separated.
	We are looking for `AF_EXAC` data within INFO. If `AF_EXAC` is not present, we skip the line
		If the value of `AF_EXAC` is >= 0.0001, then we `return` an empty `list`
		else, we `return` a `list` of the disease names from CLNDN
	
`disease_counter`
	takes a `list`, from `parse_line`, as an argument
  takes a `dictionary` from `read_file`, as a second argument
	compare the values of the `list` to the existing keys of the `dictionary`
		Take the first value of the `list` and check it against each key of the `dictionary`. 
		If a match is found, increment the value of that key by `1`
		else, create a new key for the `dictionary` and set its value to `1`
		Repeat for the remaining values of the `list`
		Do not count the diseases that are:
		- `not_specified`
		- `not_provided`

# Successes
Overall, we were very successful with this project. The outline we wrote out during our initial meeting proved to be a helpful guide once we actually began writing code. If we were stuck on a particular step, or weren't sure where to go next, we could consult it and remind ourselves of the plan. More than anything, I think this project highlighted the importance of a planning meeting well before any code is written. Our final program functions as desired, printing a dictionary where the keys are the disease names that met the criteria, and the values are the number of instances each disease appeared in the file.

# Struggles
A major struggle for us came down to being unfamiliar with RStudio. Neither of us knew how to use the debugger for it, so while we were troubleshooting our code, we found that there were times where we had to print variables at specific steps, or otherwise temporarily change outputs just so we could tell what was going on. It felt a little clunky. I think it is crucial to develop an efficient testing and debugging process.

# Personal Reflections
## Group Leader
I thought this was a great first project. I've never worked with Github before, or done any kind of collaborative code. It's a skill that I want to build, and this was a good introduction to it. The code itself didn't feel insurmountable, but my Python was a little rusty. I was frequently pausing to search for specific functions I knew existed, but couldn't remember how to use. I had lots of vague ideas of how to tackle the project, and being able to talk with another person, in addition to writing an outline, help clarify the vision.

## Other member
I've started to appreciate the value of Marcus having us work on the assignment in pairs and do peer reviews. While working on the assignment, I noticed that Chris's approach to the problem was different from my own, and his logical, layered method was very inspiring. It made me realize that I sometimes "skip steps" in my own thinking and need to trace my logic more carefully to avoid gaps in my reasoning.
I'm also new to GitHub, and I'm glad I got hands-on experience with a teammate; it's difficult to truly understand how it's used for team collaboration just by practicing on my own. This assignment also showed me that my Python skills aren't as proficient as they should be. Since I've heard that nowadays LeetCode is still often used in bioinformatician interviews, I know I have a lot of room for further practice.

# Generative AI Appendix
When writing the following parts of our program, we couldn't remember the specific syntax, so we used Google and Gemini to search for available functions or to debug.
	with open(file_path, 'r') as vcf_file:
	.startswith()
 	if diseases in key_dict_disease and diseases not in no_count:
