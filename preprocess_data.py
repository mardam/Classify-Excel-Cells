from load_data import *

def getHighestColumnNumber(rows):
    maxIndex = -1
    for row in rows:
        for cell in row:
            if (cell.column_number > maxIndex):
                maxIndex = cell.column_number
    return(maxIndex)
            

def getEmptyCellData():
    with open("empty_cell.csv") as csvfile:
        datareader = csv.reader(csvfile, delimiter = ',', quotechar = '\'')
        return(next(datareader))

emptyCellData = getEmptyCellData()
print(len(emptyCellData))

def createEmptyCell(emptyCellData, rowNumber, columnNumber, label, file, sheetName, corpus):
    emptyCellData[49] = label
    emptyCellData[24] = rowNumber
    emptyCellData[25] = columnNumber
    emptyCellData[0] = file
    emptyCellData[1] = corpus
    emptyCellData[2] = sheetName
    emptyCellData[5] = "(" + str(columnNumber) + "," + str(rowNumber) + ")"
    return(Cell(emptyCellData, label))

def padRows(rows, maxLength):
    newRows = []
    for row in rows:
        rowNumber = row[0].row_number
        sheetName = row[0].sheet_name
        file = row[0].file
        corpus = row[0].corpus
        newRow = [createEmptyCell(emptyCellData, rowNumber, -1, Strings.start_cell, file, sheetName, corpus)]
        oldIndex = 0
        nextCell = row[oldIndex]
        i = 0
        while i <= maxLength + 1:
            if nextCell.column_number == i:
                newRow.append(nextCell)
                oldIndex = oldIndex + 1
                if oldIndex < len(row):
                    nextCell = row[oldIndex]
                else:
                    i = i + 1
                    newRow.append(createEmptyCell(emptyCellData, rowNumber, i, Strings.end_cell, file, sheetName, corpus))
            else:
                newRow.append(createEmptyCell(emptyCellData, rowNumber, i, Strings.empty_cell, file, sheetName, corpus))
            i = i + 1
        newRows.append(newRow)
    return(newRows)

emptyCell = createEmptyCell(emptyCellData, 2,2, Strings.empty_cell, "abc", "def", "fgh")

print("Empty cell features:" + str(emptyCell.features) + "; length = " + str(len(emptyCell.features)))

def normalizeData(rows):
    numberOfFeatures = len(rows[0][0].features)
    for i in range(0, numberOfFeatures):
        maximum = -1
        for row in rows:
            for cell in row:
                if cell.features[i] > maximum:
                    maximum = cell.features[i]
        if maximum == -1:
            raise Exception("no maximum found")
        if maximum == 0:
            warnings.warn("Maximum == 0, " + str(i))
        else:
            for row in rows:
                for cell in row:
                    cell.features[i] = cell.features[i] / maximum
    return(rows)




