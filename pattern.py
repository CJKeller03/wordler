from dataclasses import dataclass
import functools
from pprint import pprint
import time
import numpy as np

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.8f} seconds")
        return value
    return wrapper_timer

def wordToDict(word):
    res = {}
    for letter in word:
        if not letter in res:
            res[letter] = 0
        res[letter] += 1
    return res
            
def patternFromWords(word1, word2):    
    word2Dict = wordToDict(word2)
    pattern = np.zeros(min(len(word1), len(word2)))
    for i, (letter1, letter2) in enumerate(zip(word1, word2)):
        if letter1 == letter2:
            pattern[i] = 2
            word2Dict[letter1] -= 1
        else:
            if letter1 in word2Dict and word2Dict[letter1] > 0:
                pattern[i] = 1
                word2Dict[letter1] -= 1
            else:
                pattern[i] = 0

    return pattern

def patternMatch(word1, word2, pattern):
    mask = patternFromWords(word1, word2)
    minLen = min(len(mask), len(pattern))
    return np.equal(mask[:minLen], pattern[:minLen]).all()

#@timer
def allMatches(word1, pattern, wordlist):
    return filter(lambda x: patternMatch(word1, x, pattern), wordlist)

def getWordPatternMatrix(wordlist):
    PATTERN_LENGTH = len(wordlist[0])
    


if __name__ == '__main__':
    from wordlist import GUESSES

    tmp = patternFromWords("", "belac")
    print(tmp)
    
    pprint([x for x in allMatches("", patternFromWords("", "zormesanyd"), GUESSES)])
