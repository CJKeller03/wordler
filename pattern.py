from dataclasses import dataclass
import functools
from pprint import pprint
import time
import numpy as np
from tree import Node

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

def weakPatternMatch(word1, word2, pattern):
    mask = patternFromWords(word1, word2)
    minLen = min(len(mask), len(pattern))
    return not np.isin(2, np.abs(np.subtract(mask[:minLen], pattern[:minLen])))

#@timer
def allMatches(word1, pattern, wordlist):
    return filter(lambda x: patternMatch(word1, x, pattern), wordlist)

@timer
def allMatchesCount(word1, pattern, wordlist):
    return sum([1 for _ in allMatches(word1, pattern, wordlist)])

@timer
def treeMatchCount(word1, pattern, node):
    def iterateSubnodes(node):
        matches = 0
        for subnode in node.subnodes.values():
            matches += getCount(subnode)
        #print(matches, " matches after iterating")
        return matches
    
    def getCount(node):
        #print("counting ", node.value, " (", node.isLeaf, ")...")
        matches = 0

        if node.isLeaf:
            if not patternMatch(word1, node.value, pattern):
                #print("failed a")
                return matches
            matches += iterateSubnodes(node) + 1
        
        else:
            if not weakPatternMatch(word1, node.value, pattern):
                #print("failed b")
                return matches
            matches += iterateSubnodes(node)           


        return matches
    
    return getCount(node)
    


def getWordPatternMatrix(wordlist):
    PATTERN_LENGTH = len(wordlist[0])
    


if __name__ == '__main__':
    from wordlist import GUESSES

    tmp = patternFromWords("crane", "nails")
    print(tmp)
    
    #pprint([x for x in allMatches("", patternFromWords("", "zormesanyd"), GUESSES)])

    top = Node("")
    for word in GUESSES:
        top.add(word)

    print(allMatchesCount("crane", tmp, GUESSES))
    print(treeMatchCount("crane", tmp, top))

    #print(weakPatternMatch("zzz", "aaa", tmp))
