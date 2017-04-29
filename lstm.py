from keras.models import Sequential
from keras.layers import Dense
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.utils import np_utils
from keras.layers import Dropout
from preprocess_data import *
import random
from print_results import *
from itertools import compress
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel

rows = parseCsvFile()
maxLength = getHighestColumnNumber(rows)
print("Length of longest row" + str(maxLength))
print("Full cell features:" + str(rows[0][0].features) + "; length = " + str(len(rows[0][0].features)))

normalizedRows = padRows(rows, maxLength)

print("rows_padded")
del rows

normalizedRows = normalizeData(normalizedRows)

print("rows_normalized")

number_of_features = len(normalizedRows[0][0].features)
print("Number of features: " + str(number_of_features))

batch_size = len(normalizedRows[0])



saveData(normalizedRows)

def classLabelToNumber(label):
    if label == Strings.start_cell:
        return(0)
    if label == Strings.empty_cell:
        return(1)
    if label == Strings.end_cell:
        return(2)
    if label == Strings.attributes:
        return(3)
    if label == Strings.data:
        return(4)
    if label == Strings.header:
        return(5)
    if label == Strings.metadata:
        return(6)
    if label == Strings.derived:
        return(7)
    raise Exception("Illegal classname: " + label)

euses_files = set()
enron_files = set()
fuse_files = set()

for row in normalizedRows:
    first_cell = row[0]
    if first_cell.corpus == "ENRON":
        enron_files.add(first_cell.file)
    elif first_cell.corpus == "FUSE":
        fuse_files.add(first_cell.file)
    elif first_cell.corpus == "EUSES":
        euses_files.add(first_cell.file)
    elif True:
        raise(Exception("Unknown corpus: " + first_cell.file))

print("Number of Enron Files: " + str(len(enron_files)))
print("Number of Fuse Files: " + str(len(fuse_files)))
print("Number of Euses Files: " + str(len(euses_files)))

X = []
Y = []

for row in normalizedRows:
    for cell in row:
        X.append(cell.features)
        Y.append(classLabelToNumber(cell.label))

numpy.random.seed(7)


clf = ExtraTreesClassifier()
clf = clf.fit(X, Y)

model = SelectFromModel(clf, prefit = True)
X = model.transform(X)

printFeatureWeights(clf.feature_importances_, model.get_support(), "features_selection_tree_based.txt")

print("feature selected")

for row in normalizedRows:
    for cell in row:
        cell.features = numpy.array(cell.features)[numpy.array(model.get_support())]
        #list(compress(cell.features, model.get_support()))

print("features filtered")

number_of_features = len(normalizedRows[0][0].features)

seeds = [7,15,37]
epoch_numbers = [10,20,30,50,100]
for seed in seeds:
    numpy.random.seed(seed)

    random.seed(seed)
    test_set = set(random.sample(enron_files, round(len(enron_files) / 3))).union(set(random.sample(fuse_files, round(len(fuse_files) / 3)))).union(set(random.sample(euses_files, round(len(euses_files) / 3))))
    print("Length of Test set: " + str(len(test_set)))

    trainX = []
    trainY = []
    testX = []
    testY = []
    
    for row in normalizedRows:
        for cell in row:
            if cell.file in test_set:
                testX.append(cell.features)
                testY.append(classLabelToNumber(cell.label))
            else:
                trainX.append(cell.features)
                trainY.append(classLabelToNumber(cell.label))

    X = numpy.reshape(trainX, (len(trainX), 1, number_of_features))
    y = np_utils.to_categorical(trainY)

    tX = numpy.reshape(testX, (len(testX), 1, number_of_features))
    ty = np_utils.to_categorical(testY)
    for epoch_number in epoch_numbers:
        model = Sequential()
        model.add(LSTM(100, input_shape = (X.shape[1], X.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation = 'softmax'))
        model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
        model.fit(X, y, epochs=epoch_number, batch_size = batch_size, verbose = 2, shuffle = False)

        printEvaluation("LSTM_Dropout_tree_selection_epochs" + str(epoch_number) + "_seed" + str(seed) + ".txt", model, X, y, tX, ty, batch_size)    

