import sys
from collections import Counter

# Words list taken from https://users.cs.duke.edu/~ola/ap/linuxwords
# and post-processed to lowcase and exclude non-letter characters
with open('linuxwords.txt') as f:
    words = [line.rstrip() for line in f]


def search_words(s, soft):
    """Checks whether string s is present in the word list.

    Performs a binary search over the (sorted) list of words.
    If soft is True, then s is considered a match if it is either an exact
    match or a starting substring of a word.
    """
    left = 0
    right = len(words) - 1

    while left <= right:
        idx = (right + left) // 2
        if words[idx] == s:
            return True
        if soft and words[idx].startswith(s):
            return True
        if s > words[idx]:
            left = idx + 1
        else:
            right = idx - 1

    return False


def is_valid(s, terminal, maxwords):
    """Checks whether an anagram string is valid."""
    # Base state (empty string) is valid
    if s == '':
        return True

    # Check number of word breaks vs maxwords
    if s.count(' ') + 1 > maxwords:
        return False

    # Deduplicate word orderings by only exploring words in sorted order
    words = s.split()
    if words != sorted(words):
        return False

    # Since earlier substrings have already been checked and are presumably
    # valid, only the last token or word in the string is searched in the word
    # list.
    soft = not terminal and s[-1] != ' '
    return search_words(words[-1], soft)


def get_successors(state, maxwords):
    """Traverses state graph to find valid anagrams."""

    terminal = len(state['chars']) == 0

    # Check whether the state is invalid and should be pruned
    if not is_valid(state['anagram'], terminal, maxwords):
        return []

    # If valid terminal state, stop search and return
    if terminal:
        return [state['anagram']]

    # Continue to recursively explore subsequent states
    next_states = []

    for c in state['chars']:
        chars = state['chars'].copy()
        chars.subtract({c: 1})
        if chars[c] == 0:
            del chars[c]
        next_states.append({
            'anagram': state['anagram'] + c,
            'chars': chars,
        })

    # Add an additional next state for word breaks
    if state['anagram'] != '' and state['anagram'][-1] != ' ':
        next_states.append({
            'anagram': state['anagram'] + ' ',
            'chars': state['chars'],
        })

    anagrams = []
    for next_state in next_states:
        anagrams += get_successors(next_state, maxwords=maxwords)

    return anagrams


def find_anagrams(source, maxwords=2):
    """Returns a list of anagrams based on input string.

    Deduplicates multiple orderings of the same set of words.
    """
    chars = Counter(source.lower().replace(' ', ''))

    state = {
        'anagram': '',
        'chars': chars,
    }

    anagrams = get_successors(state, maxwords)
    anagrams.sort()
    return anagrams


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: text [maxwords]')
        sys.exit()

    source = sys.argv[1]
    if len(sys.argv) == 3:
        maxwords = int(sys.argv[2])
    else:
        maxwords = 2

    anagrams = find_anagrams(source, maxwords=maxwords)

    for a in anagrams:
        print(a)
