# Srujan R
# BT18CSE041

import time

deletion_cost = 1
insertion_cost = 1
substitution_cost = 1
transposition_cost = 1
                                    
alphabet = 94
vocab = set()


def load_dict_of_words():
    global vocab

    dict_file = open('dictionary.txt', 'r')
    words = dict_file.read().split()

    for i in words:
        if i not in vocab and len(i) > 1:
            vocab.add(i.lower())


def damerau_Levenshtein_distance_algo(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)

    dist = [[0 for j in range(str2_len + 2)] for i in range(str1_len + 2)]

    dist_alpha = {}
    for i in range(33, 127):
        dist_alpha[chr(i)] = 0

    maxdist = str1_len + str2_len
    dist[0][0] = maxdist

    for i in range(1, str1_len):
        dist[i+1][0] = maxdist
        dist[i+1][1] = i

    for j in range(1, str2_len):
        dist[0][j+1] = maxdist
        dist[1][j+1] = j

    for i in range(1, str1_len+1):
        db = 0
        cost = 0
        for j in range(1, str2_len+1):
            k = dist_alpha[str2[j-1]]
            l = db
            if str1[i-1] == str2[j-1]:
                cost = 0
                db = j
            else:
                cost = substitution_cost

            dist[i+1][j+1] = min(dist[i][j] + cost,
                                 dist[i+1][j] + insertion_cost,
                                 dist[i][j+1] + deletion_cost,
                                 dist[k][l] + (i-k-1) + (j-l-1) + transposition_cost)

        dist_alpha[str1[i-1]] = i

    return dist[str1_len + 1][str2_len + 1]


# print(damerau_Levenshtein_distance_algo("m", "morse"))

query = input("Enter your query: ").lower()

load_dict_of_words()

start = time.time()

if query in vocab:
    print("Word present in vocabulary!")
else:
    correct_word = []
    min_dist = 999999

    for i in vocab:
        dist = damerau_Levenshtein_distance_algo(query, i)
        if dist == min_dist:
            correct_word.append((i, dist))
        elif dist < min_dist:
            correct_word = [(i, dist)]
            min_dist = dist

    end = time.time()

    for i in correct_word:
        print("WORD = {}, DIST = {}".format(i[0], i[1]))

    print("Search completed in {} secs".format(end-start))
