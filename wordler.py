import functools
from genericpath import exists
from math import inf
import pprint
import time
import re

from numpy import base_repr
from wordlist import ANSWERS, GUESSES
from dataclasses import dataclass

@dataclass
class WordPattern:
    exclude: frozenset
    exist: frozenset
    known: tuple[tuple]

    @classmethod
    def fromWords(cls, word, answer):
        wSet = frozenset(word)
        aSet = frozenset(answer)
        known = []
        for (wLtr, aLtr) in zip(word, answer):
            if wLtr == aLtr:
                known.append((1, wLtr))
            else:
                known.append((-1, wLtr))

        return WordPattern(frozenset(wSet.difference(aSet)), frozenset(wSet.intersection(aSet)), tuple(known))

    @classmethod
    def fromMask(cls, word, mask):
        exclude = set([])
        exist = set([])
        known = []
        for (wLtr, key) in zip(word, mask):
            if key == '0' and wLtr not in exist:
                exclude.add(wLtr)
                known.append((-1, wLtr))
            elif key == '1' and wLtr not in exclude:
                exist.add(wLtr)
                known.append((-1, wLtr))
            elif wLtr not in exclude:
                exist.add(wLtr)
                known.append((1, wLtr))
        
        if len(known) < 5:
            return None
        
        return WordPattern(frozenset(exclude), frozenset(exist), tuple(known))


    def check(self, word):
        tmp = set()
        matches = 0
        for i, (cLet, kLet) in enumerate(zip(word, self.known)):
            if (kLet[0] == 1) != (kLet[1] == cLet):
                return False
            elif cLet in self.exclude:
                return False

            if cLet in self.exist and cLet not in tmp:
                tmp.add(cLet)
                matches += 1

        if len(tmp) < len(self.exist):
            return False

        return True

    def __eq__(self, __o: object) -> bool:
        return (isinstance(__o, WordPattern) and 
               __o.exclude == self.exclude and 
               __o.exist == self.exist and 
               __o.known == self.known)

    
    def __hash__(self) -> int:
        return self.exclude.__hash__() * self.exist.__hash__() * self.known.__hash__()

    def __str__(self) -> str:
        return "WordPattern {3} excludes {0}, contains {1}, and matches {2}".format(
            self.exclude.__str__(),
            self.exist.__str__(),
            self.known,
            self.__hash__()
        )

            


#ANSWERS.sort()
#GUESSES.sort()

WORDS = ANSWERS + GUESSES
WORDS.sort()

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

#@timer
def inList(word, list):
    def x(word, list, start, end):
        cur = start + (end - start) // 2
        if (curWord := list[cur]) == word:
            return cur
        else:
            return x(word, list, start, cur) if curWord > word else x(word, list, cur, end)
    
    return x(word, list, 0, len(list) - 1)

def getRegex(exclude, exist, certain):
    fail = re.compile("[{0}]".format("".join(exclude))) if exclude else None
    exString = "".join(["(?=.*{0})".format(x) for x in exist])
    certainString = "".join([x if x != -1 else "." for x in certain])
    good = re.compile(exString + certainString)

    return (fail, good)

#@timer
def getWords(regex):
    return list(filter(lambda x: regex.match(x), WORDS))

#@timer
def getMatches(fail, good, words):
    return list(filter(lambda x: not fail.match(x) if fail else True, filter(lambda x: good.match(x), words)))

def countMatches(fail, good, words):
    count = 0
    for word in words:
        if (fail and not fail.match(word)) and good.match(word):
            count += 1
    return count

#@timer
def analyzeGuess(word, answer):
    exclude = set()
    exist = set()
    certain = [-1, -1, -1, -1, -1]
    for i, letter in enumerate(word):
        if word[i] == answer[i]:
            certain[i] = letter
        else:
            if letter in answer:
                exist.add(letter)
            else:
                exclude.add(letter)
    return (exclude, exist, certain)

@timer
def chooseGuess(possible):
    best = inf
    bestGuess = ""
    for answer in possible:
        @timer
        def temp(best, bestGuess):
            for guess in WORDS:
                fail, good = getRegex(*analyzeGuess(guess, answer))
                matches = countMatches(fail, good, possible)
                score = abs(0.5 - matches / len(possible))
                if score < best:
                    best = score
                    bestGuess = guess
        temp(best, bestGuess)
        print(answer)
    return bestGuess, best

#print(inList("twyer", WORDS))

#exclude, include = getRegex(["g", "f", "o"], ["a"], [-1, "e", -1, -1, -1])

#print(getMatches(exclude, include))

#print(chooseGuess(WORDS))

#p = WordPattern.fromWords("caleb", "kales")

def genMasks():
    base = 3
    size = 5
    for i in range(base ** size):
        yield base_repr(i, base).rjust(size, "0")

tmp = {}

for guess in WORDS:
    #print(guess)
    for mask in genMasks():
        p = WordPattern.fromMask(guess, mask)
        #print(p)
        if p and p not in tmp:
            res = filter(p.check, WORDS)
            tmp[p] = res

print("done")

#sortedTmp = list(tmp)
#sortedTmp = [(p, list(x)) for (p, x) in tmp]
#sortedTmp.sort(lambda x: len(x[1]))

#pprint.pprint(tmp)
#print(timer(lambda:list(filter(p.check, WORDS)))())

for key, val in tmp.items():
    print(key, " -> ", sum([1 for _ in val]))
