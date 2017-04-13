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

def printEvaluation(fileName, model, Xtrain, Ytrain, Xtest, Ytest):
    file = open("C:/Users/Markus Damm/Programmierung/Classify-Excel-Cells/outputs/" + fileName, "w+")
    scores = model.evaluate(tX, ty, verbose = 0, batch_size = batch_size)
    file.write("Model Accuracy: %.2f%%" % (scores[1]*100))

    file.write("Training:\n")
    ypred = numpy.argmax(model.predict(Xtrain), axis = 1)
    file.write("----------------------------------\n")
    file.write("Confusion matrix:\n")
    file.write(str(confusion_matrix(numpy.argmax(Ytrain, axis = 1), ypred)))
    file.write("\n\n-----------------------------------\n")
    file.write("Metics:")
    file.write(str(classification_report(numpy.argmax(Ytrain, axis = 1), ypred)))

    file.write("Test:")
    ypred = numpy.argmax(model.predict(Xtest), axis = 1)
    file.write("----------------------------------\n")
    file.write("Confusion matrix:\n")
    file.write(str(confusion_matrix(numpy.argmax(Ytest, axis = 1), ypred)))
    file.write("\n\n-----------------------------------\n")
    file.write("Metics:\n")
    file.write(str(classification_report(numpy.argmax(Ytest, axis = 1), ypred)))
    file.close()
    

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

epochNumbers = [300, 400, 500]
for number in epochNumbers:
    print("##############################################")
    print("Number of epochs: " + str(number))
    model = Sequential()
    model.add(LSTM(40, input_shape = (X.shape[1], X.shape[2])))
    model.add(Dense(y.shape[1], activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
    model.fit(X, y, epochs=number, batch_size = batch_size, verbose = 2, shuffle = False)
    printEvaluation("LSTM_" + str(number) + ".txt", model, X, y, tX, ty)

epochNumbers = [1000]
for number in epochNumbers:
    print("##############################################")
    print("Number of epochs: " + str(number))
    model = Sequential()
    model.add(SimpleRNN(40, input_shape = (X.shape[1], X.shape[2])))
    model.add(Dense(y.shape[1], activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
    model.fit(X, y, epochs=number, batch_size = batch_size, verbose = 2, shuffle = False)
    printEvaluation("RNN_" + str(number) + ".txt", model, X, y, tX, ty)

