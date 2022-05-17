import nltk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from IPython.display import display


#download the treebank corpus from nltk
nltk.download('treebank')
 
#download the universal tagset from nltk
nltk.download('universal_tagset')
 
# reading the Treebank tagged sentences
nltk_data = list(nltk.corpus.treebank.tagged_sents(tagset='universal'))

# split data into training and validation set in the ratio 80:20
train_set,test_set = train_test_split(nltk_data,train_size=0.80,test_size=0.20,random_state = 101)

# create list of train and test tagged words
train_tagged_words = [ tup for sent in train_set for tup in sent ]
test_tagged_words = [ tup for sent in test_set for tup in sent ]

print("\n\t\t\t\t-----TAG INFO-----\n")

# use set datatype to check how many unique tags are present in training data
tags = {tag for word,tag in train_tagged_words}
print("Number of Tags:", len(tags))
print("Unique Tags:", tags)


# compute Emission Probability
def word_given_tag(word, tag, train_bag = train_tagged_words):
    tag_list = [pair for pair in train_bag if pair[1]==tag]

    # total number of times the passed tag occurred in train_bag
    count_tag = len(tag_list)
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0]==word]

    # now calculate the total number of times the passed word occurred as the passed tag.
    count_w_given_tag = len(w_given_tag_list)
 
    return (count_w_given_tag, count_tag)

# compute  Transition Probability
def t2_given_t1(t2, t1, train_bag = train_tagged_words):
    tags = [pair[1] for pair in train_bag]

    count_t1 = len([t for t in tags if t==t1])
    count_t2_t1 = 0

    for index in range(len(tags)-1):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1

    return (count_t2_t1, count_t1)

def Viterbi(words, train_bag = train_tagged_words):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
     
    for key, word in enumerate(words):
        # initialise list of probability column for a given observation
        p = [] 
        for tag in T:
            if key == 0:
                transition_p = tags_df.loc['.', tag]
            else:
                transition_p = tags_df.loc[state[-1], tag]
                 
            # compute emission and state probabilities
            word_given_tag_p = word_given_tag(words[key], tag)
            emission_p = word_given_tag_p[0]/word_given_tag_p[1]
            state_probability = emission_p * transition_p    
            p.append(state_probability)
             
        pmax = max(p)

        # getting state for which probability is maximum
        state_max = T[p.index(pmax)] 
        state.append(state_max)

    return list(zip(words, state))


# creating t x t transition matrix of tags, t = no of tags where Matrix(i, j) represents P(jth tag after the ith tag)
tags_matrix = np.zeros((len(tags), len(tags)), dtype='float32')

for i, t1 in enumerate(list(tags)):
    for j, t2 in enumerate(list(tags)): 
        tags_matrix[i, j] = t2_given_t1(t2, t1)[0]/t2_given_t1(t2, t1)[1]

print("\n\t\t\t\t-----TRANSITION MATRIX OF TAGS-----\n")

# convert the matrix to a df 
tags_df = pd.DataFrame(tags_matrix, columns = list(tags), index=list(tags))
display(tags_df)

# list of 5 sentences on which we test the model
test_run = ["I should write something easy to read",
            "John is concerned about the examples",
            "Are the questions being asked too complex ?",
            "Mary is playing football with her friends",
            "Paris is the capital of France"]

print("\n\t\t\t\t-----OUTPUT-----\n") 

for i in range(5):
    print("Sentence: ", test_run[i])

    prediction = Viterbi(test_run[i].split(" "))

    print("Predicted Tags: ", prediction)

    print("\t\t\t\t----------")