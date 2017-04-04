import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.utils import np_utils
from preprocess_data import *
from sklearn.metrics import confusion_matrix, classification_report

rows = parseCsvFile()
maxLength = getHighestColumnNumber(rows)
print("Length of longest row" + str(maxLength))
print("Full cell features:" + str(rows[0][0].features) + "; length = " + str(len(rows[0][0].features)))

paddedRows = padRows(rows, maxLength)

normalizedRows = normalizeData(paddedRows)

#for row in normalizedRows:
#    for cell in row:
#        cell.features = cell.features[1:4]

number_of_features = len(normalizedRows[0][0].features)
print("Number of features: " + str(number_of_features))

batch_size = len(normalizedRows[0])

trainX = []
trainY = []
testX = []
testY = []

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
        if cell.corpus == "ENRON":
            testX.append(cell.features)
            testY.append(classLabelToNumber(cell.label))
        else:
            trainX.append(cell.features)
            trainY.append(classLabelToNumber(cell.label))

numpy.random.seed(7)


X = numpy.reshape(trainX, (len(trainX), 1, number_of_features))
y = np_utils.to_categorical(trainY)

tX = numpy.reshape(testX, (len(testX), 1, number_of_features))
ty = np_utils.to_categorical(testY)

model = Sequential()
model.add(SimpleRNN(40, input_shape = (X.shape[1], X.shape[2])))
model.add(Dense(y.shape[1], activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
model.fit(X, y, epochs=3, batch_size = batch_size, verbose = 2, shuffle = False)



scores = model.evaluate(tX, ty, verbose = 0, batch_size = batch_size)
print("Model Accuracy: %.2f%%" % (scores[1]*100))

ypred = numpy.argmax(model.predict(tX), axis = 1)
print("----------------------------------")
print("Confusion matrix:")
print(confusion_matrix(numpy.argmax(ty, axis = 1), ypred))
print("\n\n-----------------------------------")
print("Metics:")
print(classification_report(numpy.argmax(ty, axis = 1), ypred))
