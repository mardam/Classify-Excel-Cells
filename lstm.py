import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import SimpleRNN
from keras.utils import np_utils
from preprocess_data import *

rows = parseCsvFile()
maxLength = getHighestColumnNumber(rows)
print("Length of longest row" + str(maxLength))
print("Full cell features:" + str(rows[0][0].features) + "; length = " + str(len(rows[0][0].features)))

paddedRows = padRows(rows, maxLength)

normalizedRows = normalizeData(rows)

#for row in normalizedRows:
#    for cell in row:
#        cell.features = cell.features[1:4]

number_of_features = len(normalizedRows[0][0].features)
print("Number of features: " + str(number_of_features))

batch_size = len(normalizedRows[0])

dataX = []
dataY = []

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

for row in normalizedRows:
    for cell in row:
        dataX.append(cell.features)
        dataY.append(classLabelToNumber(cell.label))

numpy.random.seed(7)


X = numpy.reshape(dataX, (len(dataX), 1, number_of_features))
y = np_utils.to_categorical(dataY)


model = Sequential()
model.add(SimpleRNN(32, input_shape = (X.shape[1], X.shape[2])))
model.add(Dense(y.shape[1], activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
model.fit(X, y, epochs=2, batch_size = batch_size, verbose = 2, shuffle = False)

scores = model.evaluate(X, y, verbose = 0)
print("Model Accuracy: %.2f%%" % (scores[1]*100))
