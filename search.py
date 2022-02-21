from platform import node
from tree import Node
from wordlist import GUESSES
from pattern import *

def safeLog2(x):
    if x == 0:
        return 0
    return np.log2(1/x)

def prunedTreeSearch(wordlist, pattern):
    #optimalMatches = round(0.3679 / len(wordlist)) / len(wordlist)
    tree = Node("")
    TOTAL_WORDS = len(wordlist)
    for word in wordlist:
        tree.add(word)

    nodesSkipped = 0

    def search(node, pattern, maxInformation = 0, minMatches = TOTAL_WORDS):
        nonlocal nodesSkipped
        #print("searching node: ", node.value)
        MATCHES = sum([1 for _ in allMatches(node.value, pattern, wordlist)])
        PERCENT_MATCH = MATCHES / TOTAL_WORDS
        
        #print("cur matches: ", PERCENT_MATCH)
        curInformation = PERCENT_MATCH * safeLog2(PERCENT_MATCH)
        #print("cur info: ", curInformation)

        if curInformation < maxInformation and MATCHES < minMatches:
            nodesSkipped += len(node) - 1
            return maxInformation, None, minMatches


        bestInformation = curInformation if node.isLeaf else 0
        bestValue = node.value if node.isLeaf else None
        bestMatches = MATCHES if node.isLeaf else TOTAL_WORDS

        for subnode in node.subnodes.values():
            subnodeInformation, subnodeBestValue, subnodeBestMatches = search(subnode, pattern, bestInformation, bestMatches)
            if subnodeInformation > bestInformation:
                bestInformation = subnodeInformation
                bestValue = subnodeBestValue
                bestMatches = subnodeBestMatches

        print("best info and node for ", node.value, " is ", bestInformation, ", ", bestValue, " -- skipped: ", nodesSkipped)  
        return bestInformation, bestValue, bestMatches
    

    return search(tree, pattern)


def exhaustiveSearch(wordlist, pattern):
    TOTAL_WORDS = len(wordlist)
    bestInformation = 0
    bestWord = None
    for word in wordlist:
        PERCENT_MATCH = sum([1 for _ in allMatches(word, pattern, wordlist)]) / TOTAL_WORDS
        curInformation = PERCENT_MATCH * safeLog2(PERCENT_MATCH)
        if curInformation > bestInformation:
            bestInformation = curInformation
            bestWord = word
    return bestWord, bestInformation

if __name__ == '__main__':
    pattern = patternFromWords("zzezz", "eaaaa")
    print(pattern)
    #print(sum([1 for _ in allMatches("b", pattern, GUESSES)]) / len(GUESSES))
    #print(exhaustiveSearch(GUESSES, pattern))
    print(prunedTreeSearch(GUESSES, pattern))