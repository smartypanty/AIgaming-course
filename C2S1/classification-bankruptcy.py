import numpy as np
import re


# parsing input file into an array
file = open('/Users/smartypants/Desktop/my docs/AI Gaming/my materials/C2S1/bankruptcy_dataset.txt', 'r')
input = file.read()

input = input.replace('NB', '1')
input = input.replace('P', '2')
input = input.replace('A', '1')
input = input.replace('N', '0')
input = input.replace('B', '2')

instance_strings = input.splitlines()
print(len(instance_strings))  # 250 instances

np.random.shuffle(instance_strings) # important for train-test

instances = []
for s in instance_strings:
    instance = re.split(r",", s)
    instances.append(instance)
print(len(instances))


# creating a dataset
data = []
targets = []

for i in instances:
    instance_data = i[:6]
    data.append(instance_data)
    target = i[6]
    targets.append(target)

print(len(targets))
print(len(data))

target_names = ['bankrupt', 'not-bankrupt']


dataset = {
    u'data': data,
    u'targets':targets,
    u'target_names':target_names
}
#print(dataset)

dataset_X = dataset.get('data')
dataset_Y = dataset.get('targets')
print(np.unique(dataset_Y))


# train and test sets

dataset_X_train = dataset_X[:225] # 90% for training
dataset_Y_train = dataset_Y[:225]
dataset_X_test  = dataset_X[225:] # 10% for testing
dataset_Y_test  = dataset_Y[225:]


# train a model
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier()

model.fit(dataset_X_train, dataset_Y_train)

#test
predictions = model.predict(dataset_X_test)
#print(knn.predict(dataset_X_test))
#print(dataset_Y_test)

for i in range(25):
    print(predictions[i])
    print(dataset_Y_test[i])