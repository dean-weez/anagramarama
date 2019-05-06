import sys
from collections import Counter

# Words list taken from https://users.cs.duke.edu/~ola/ap/linuxwords
# and post-processed to lowcase and exclude non-letter characters
with open('linuxwords.txt') as f:
    words = [line.rstrip() for line in f]

def search_words(s, soft):
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


def is_valid(s, terminal):
    if s == '':
        return True

    token = s.split()[-1]
    soft = not terminal and s[-1] != ' '
    return search_words(token, soft)


def get_successors(state, maxwords=2):
    if state['anagram'].count(' ') + 1 > maxwords:
        return []

    terminal = len(state['chars']) == 0
    if not is_valid(state['anagram'], terminal):
        return []
    if terminal:
        return [state['anagram']]
    
    next_states = []

    for c in state['chars']:
        chars = state['chars'].copy()
        chars.subtract({c:1})
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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: word [maxwords]')
        sys.exit()

    source = sys.argv[1]
    if len(sys.argv) == 3:
        maxwords = int(sys.argv[2])
    else:
        maxwords = 2

    chars = Counter(source.lower().replace(' ', ''))

    state = {
        'anagram': '',
        'chars': chars,
    }

    anagrams = get_successors(state, maxwords=maxwords)
    for a in anagrams:
        print(a)

