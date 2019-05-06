# anagramarama

This script finds anagrams of an input string. Try your name! You may discover a fun new alter ego.

## Usage
`python anagrams.py TEXT [MAX_WORDS]`

The `TEXT` input is case insensitive and may include whitespace. Inputs with numbers or symbols will return no matches.

By default, only anagrams of up to 2 words are returned, but this can be adjusted with the `MAX_WORDS` parameter.

Note that the runtime _rapidly_ increases with the length of the input and max words, like O(N!).

## How it works

Instead of checking the full n! permutations of the input, the script constructs a state graph of anagram string and remaining letters and searches the graph for valid anagrams, pruning branches as it goes if an invalid state is encoutered (if the start of an anagram string doesn't match the start of a known word, then any longer anagram string will also not match).

## TODO

If a string S has an anagram consisting of multiple words, then all orderings of those words will also be anagrams of S. This means that outputs may have near-duplicate results of the form "A B" and "B A". The script output could be made more parsimonious by only returning unique _sets_ of words.

As the graph search fans out, each branch is traversed independently; as such, this is an ideal problem for parallelization. Running on multiple threads would decrease runtime for longer input strings.
