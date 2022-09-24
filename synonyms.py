'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    denominator, numerator = 0, 0
    denominator = norm(vec1) * norm(vec2)

    for key1 in vec1:
        for key2 in vec2:
            if key1 == key2:
                numerator += vec1[key1] * vec2[key2]

    return numerator / denominator


def build_semantic_descriptors(sentences):
    # set up return variable
    d = {}

    # for each sentences, check for each unique individual words
    for sentence in sentences:
        checked_word = []  # list for unique words
        for word in sentence:  # set each word of the sentence as the index
            if word in checked_word:
                continue  # word already checked in this sentence, check for the next word
            checked_word.append(word)
            if word not in d:
                d[word] = {}  # add word as key in d
            checked_descriptor = []  # list for unique descriptors
            for descriptor in sentence:
                if descriptor in checked_descriptor:
                    continue  # descriptor already checked in this sentence, check for next descriptor
                if word != descriptor:  # check if descriptor is not the same as word (index)
                    checked_descriptor.append(descriptor)
                    if descriptor not in d[word]:
                        d[word][descriptor] = 1  # create a descriptor key in the index
                    else:
                        d[word][descriptor] += 1  # another sentence where index and descriptor appear together
    return d


def build_semantic_descriptors_from_files(filenames):
    d = {}
    punc_to_remove = [",", "-", "--", ":", ";"]
    punc_to_new = [".", "!", "?"]
    for f in filenames:
        file = open(f, "r", encoding="latin1")
        text = file.read().lower()
        file.close()
        # remove meaningless punctuations
        for element in punc_to_remove:
            text = text.replace(element, " ")
        # separate sentences
        for element in punc_to_new:
            text = text.replace(element, "\n")
        sentence_list = text.split("\n")
        # separate words from sentences
        for i in range(len(sentence_list)):
            sentence_list[i] = sentence_list[i].split()
        # utilize build_semantic_descriptors()
        sd = build_semantic_descriptors(sentence_list)
        # add things to d
        for word in sd:
            if word not in d:
                d[word] = sd[word]
            else:
                for descriptor in sd[word]:
                    if descriptor in d[word]:
                        d[word][descriptor] += 1
                    else:
                        d[word][descriptor] = 1
    return d


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    semantic_similarity = []
    for choice in choices:
        if choice not in semantic_descriptors:
            semantic_similarity.append(-1)  # not comparable
        else:
            semantic_similarity.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choice]))
    rank = sorted(semantic_similarity, reverse=True)  # biggest is first, index of the biggest
    return choices[semantic_similarity.index(rank[0])]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    total = 0
    correct = 0

    file = open(filename, "r", encoding="latin1")
    while file.readable():
        line = file.readline().split()
        if line:  # there exists things in line
            synonym = line[0]
            answer = line[1]
            question = line[2:]
            total += 1

            response = most_similar_word(synonym, question, semantic_descriptors, similarity_fn)
            if response == answer:
                correct += 1
        else:
            break  # file is still readable, but no more new lines, exits the while loop
    return correct / total * 100.0  # in percentage


if __name__ == "__main__":
    files = ["casenovel1.txt", "casenovel2.txt"]
    des = build_semantic_descriptors_from_files(files)
    print(str(run_similarity_test("test.txt", des, cosine_similarity)) + "% of the guesses were correct")
