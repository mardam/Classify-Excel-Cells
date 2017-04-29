from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support
import numpy

def calculateWeightedMeasure(measures, supports):
	if len(measures) != len(supports):
		raise(Exception("blub"))
	ret = 0
	sum = 0
	for i in range(0, len(measures)):
		sum = sum + supports[i]
		ret = ret + (measures[i] * supports[i])
	return(ret / sum)

def calculateAllWeightedMeasuresInRelevants(measures, lower = 3, upper = 8):
    length = len(measures)
    supports = measures[length - 1].tolist()[lower:upper]
    ret = []
    for i in range(0,length - 1):
        ret.append(calculateWeightedMeasure(measures[i].tolist()[lower:upper], supports))
    return(ret)

def printEvaluation(fileName, model, Xtrain, Ytrain, Xtest, Ytest, batch_size):
    file = open("outputs/" + fileName, "w+")
    scores = model.evaluate(Xtest, Ytest, verbose = 0, batch_size = batch_size)
    file.write("Model Accuracy: %.2f%%" % (scores[1]*100))

    file.write("Training:\n")
    ypred = numpy.argmax(model.predict(Xtrain), axis = 1)
    file.write("----------------------------------\n")
    file.write("Confusion matrix:\n")
    file.write(str(confusion_matrix(numpy.argmax(Ytrain, axis = 1), ypred)))
    file.write("\n\n-----------------------------------\n")
    file.write("Metrics:\n")
    file.write(str(classification_report(numpy.argmax(Ytrain, axis = 1), ypred)))

    file.write("Weighted measures: \n")
    file.write(str(calculateAllWeightedMeasuresInRelevants(precision_recall_fscore_support(numpy.argmax(Ytrain, axis = 1), ypred))))

    file.write("\nTest:\n")
    ypred = numpy.argmax(model.predict(Xtest), axis = 1)
    file.write("----------------------------------\n")
    file.write("Confusion matrix:\n")
    file.write(str(confusion_matrix(numpy.argmax(Ytest, axis = 1), ypred)))
    file.write("\n\n-----------------------------------\n")
    file.write("Metrics:\n")
    file.write(str(classification_report(numpy.argmax(Ytest, axis = 1), ypred)))

    file.write("Weighted measures:\n")
    file.write(str(calculateAllWeightedMeasuresInRelevants(precision_recall_fscore_support(numpy.argmax(Ytest, axis = 1), ypred))))
    file.close()

def printFeatureWeights(featureWeights, support, file_name):
    file = open("outputs/" + file_name, "w+")
    file.write("Feature Weights: \n")
    file.write(str(featureWeights))
    file.write("\n\n\nSupport: \n\n")
    file.write(str(support))
    file.close()
    

