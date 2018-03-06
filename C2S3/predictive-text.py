import re
from copy import deepcopy


def getSequenceProbability(sequence, corpus_size, history_window, dictionary):
    if type(sequence) is not list:
        sequence = re.split(" ", sequence)

    product = 1
    for i in range(len(sequence) - history_window):
        subsequence = tuple(sequence[i:i+history_window+1])
        if subsequence in dictionary:
            count = dictionary[subsequence]
        else:
            count = 1
        product *= count/corpus_size
    return product




def generatePotentialSequences(target_words, sequence, potential_sequences):
    if "__" in sequence:
        index = sequence.index("__")
        updated_potential_sequencies = []
        for potential_sequence in potential_sequences:
            for target_word in target_words:
                potential_sequence[index] = target_word
                updated_potential_sequencies.append(deepcopy(potential_sequence))
        sequence[index] = "filled"
        potential_sequences = generatePotentialSequences(target_words, sequence, updated_potential_sequencies)
    return potential_sequences



def predictWords(target_words, sequence, corpus_size, history_window, dictionary):
    sequence = re.split(" ", sequence)

    if "__" in sequence:

        potential_sequences = generatePotentialSequences(target_words, sequence, [sequence])


        current_highest_probability = 0
        current_best_sequence = []
        for potential_sequence in potential_sequences:
            probability = getSequenceProbability(potential_sequence, corpus_size, history_window, dictionary)
            print(potential_sequence)
            print(probability)

            if probability > current_highest_probability:
                current_highest_probability = probability
                current_best_sequence = potential_sequence
        return current_best_sequence

    else:
        return sequence



#########################################################

'''
# https://www.corpusdata.org/now_corpus.asp -> samples -> text
file = open('corpus.txt', 'r')
input = file.read()

corpus = re.split(" ", input)
corpus_size = len(corpus)
print(corpus_size) # 1959580


# precompute counts
sequence_counts = dict()
for i in range(corpus_size - history_window+1):
    sequence = tuple(corpus[i:i+history_window+1])
    sequence_counts[sequence] = sequence_counts.setdefault(sequence, 0) + 1
print(len(sequence_counts))

# filter counts
top_frequencies = dict()
for sequence,frequency in sequence_counts.items():
    if frequency > 1:
        top_frequencies[sequence] = frequency

file1 = open('corpus-counts.txt','w')
file1.write(str(top_frequencies))
file1.close()
'''


corpus_size = 1959580

history_window = 2
target_words = set(("of", "to", "in", "it", "if", "is", "by", "he", "on", "we", "as", "be", "up", "at"))

file2 = open('corpus-counts.txt','r')
dictionary = eval(file2.read())
print(len(dictionary))



sequence = "I want to go to London"
sequence_probability = getSequenceProbability(sequence, corpus_size, history_window, dictionary)
print(sequence_probability) #2.209791888110178e-16


sequence = "I want to __ __ London"
full_sequence = predictWords(target_words, sequence, corpus_size, history_window, dictionary)
print(full_sequence) # I want to be in London


