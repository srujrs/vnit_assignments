# Srujan R
# BT18CSE041

import time

DICTIONARY = "dictionary.txt"
TARGET = "promt"
MAX_COST = 1

class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

    def insert(self, word):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word


trie = TrieNode()
for word in open(DICTIONARY, 'r').read().split():
    trie.insert(word)

print("Creating Trie data structure for the dictionary of words")


def check_dictionary(word, maxCost):

    currentRow = range(len(word) + 1)

    results = []

    for letter in trie.children:
        find_distance(trie.children[letter], '', letter, word, [], currentRow,
                        results, maxCost)

    return results


def find_distance(node, prevLetter, letter, word, prevpreviousRow, previousRow, results, maxCost):

    columns = len(word) + 1
    currentRow = [previousRow[0] + 1]

    for column in range(1, columns):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[column - 1] + 1
        else:
            replaceCost = previousRow[column - 1]

        transposeCost = 999999

        if prevpreviousRow != [] and prevLetter != '':
            if column > 1 and word[column - 1] == prevLetter and word[column - 2] == letter:
                transposeCost = prevpreviousRow[column - 2] + 1

        currentRow.append(min(insertCost, deleteCost,
                          replaceCost, transposeCost))

    if currentRow[-1] <= maxCost and node.word != None:
        results.append((node.word, currentRow[-1]))

    prevLetter = letter

    if min(currentRow) <= maxCost:
        for letter in node.children:
            find_distance(node.children[letter], prevLetter, letter, word, previousRow, currentRow,
                            results, maxCost)


start = time.time()
results = check_dictionary(TARGET, MAX_COST)
end = time.time()

for result in results:
    print("WORD = {}, DIST = {}".format(result[0], result[1]))

print("Search completed in %g secs" % (end - start))

