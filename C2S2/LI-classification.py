import numpy as np
import re


# parsing input file into an array
file = open('/Users/smartypants/Desktop/my docs/AI Gaming/my materials/C2S2/phrases.txt', 'r')
input = file.read()
instance_strings = input.splitlines()
np.random.shuffle(instance_strings)
print(len(instance_strings))  # 250 instances


# creating a dataset
data = []
targets = []
for s in instance_strings:
    if not s.startswith("%"): # the line is not a comment with the translation
        instance = re.split("\|\|\|", s)
        data.append(instance[0].strip())
        targets.append(instance[1].strip())
print(len(data))
print(len(targets))


# splitting dataset into train and tests
train_test_ratio = 0.8
train_size = round(len(data) * train_test_ratio)

train = data[:train_size]
test  = data[train_size:]

# generating features (character trigrams)
ngrams = set()
n = 3
for s in train:
    for i in range(len(s) - n + 1):
        ngram = s[i:i+n]
        ngrams.add(ngram)
ngrams = list(ngrams)
print(len(ngrams))


# creating boolean feature vectors
dataset_X_train = []
dataset_Y_train = targets[:train_size]
dataset_X_test  = []
dataset_Y_test  = targets[train_size:]

for s in train:
    vector = []
    for ngram in ngrams:
        if ngram in s:
            vector.append(1)
        else:
            vector.append(0)
    dataset_X_train.append(vector)

for s in test:
    vector = []
    for ngram in ngrams:
        if ngram in s:
            vector.append(1)
        else:
            vector.append(0)
    dataset_X_test.append(vector)

##################################### classification ######################
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()

model.fit(dataset_X_train, dataset_Y_train)

#test
predictions = model.predict(dataset_X_test)

mistakes = 0
for i in range(len(predictions)):
    if dataset_Y_test[i] != predictions[i]:
        print(test[i] + " is " + dataset_Y_test[i])
        print("but predicted as " + predictions[i])
        mistakes += 1

print("Total number of test instances: " + str(len(dataset_Y_test)))
print("Number of misclassified instances: " + str(mistakes))