from load_data import *


def getHighestColumnNumber(rows):
    maxIndex = -1
    for row in rows:
        for cell in row:
            if (cell.column_number > maxIndex):
                maxIndex = cell.column_number
    return(maxIndex)
            

def getEmptyCellData():
    with open("empty_cell_full_features.csv") as csvfile:
        datareader = csv.reader(csvfile, delimiter = ',', quotechar = '\'')
        return(next(datareader))

emptyCellData = getEmptyCellData()
print(len(emptyCellData))

def createEmptyCell(emptyCellData, rowNumber, columnNumber, neighbors, label, file, sheetName, corpus):
    emptyCellData[config.label_position] = label
    emptyCellData[config.row_number_position] = rowNumber
    emptyCellData[config.column_number_position] = columnNumber
    emptyCellData[config.file_name_position] = file
    emptyCellData[config.corpus_name_position] = corpus
    emptyCellData[config.sheet_name_position] = sheetName
    emptyCellData[config.cell_adress_position] = "(" + str(columnNumber) + "," + str(rowNumber) + ")"
    cell = Cell(emptyCellData, label)
    #cell.setNeighbors(neighbors)
    return(cell)


def checkCellNeighborsRow(row, columnNumber):
    for cell in row:
        if cell.column_number == columnNumber:
            if cell.hasImportantClass:
                return(1)
            else:
                return(0)
        if cell.column_number > columnNumber:
            return(0)
    return(0)

def checkCellNeighborsCurrentRow(row, columnNumber):
    ret = 0
    for cell in row:
        if cell.column_number == columnNumber - 1:
            if cell.hasImportantClass:
                ret = 1
        if cell.column_number == columnNumber + 1:
            if cell.hasImportantClass:
                return(ret + 1)
            else:
                return(ret)
        if cell.column_number > columnNumber:
            return(ret)
    return(ret)
            
            

def collectNumberOfNeighbors(previousRow, currentRow, nextRow, columnNumber):
    return(checkCellNeighborsRow(previousRow, columnNumber) + checkCellNeighborsRow(nextRow, columnNumber) + checkCellNeighborsCurrentRow(currentRow, columnNumber))
        

def padRows(rows, maxLength):
    newRows = []
    oldSheetName = ""
    for j in range(0, len(rows)):
    #for row in rows:
        row = rows[j]
        rowNumber = row[0].row_number
        sheetName = row[0].sheet_name
        if oldSheetName == sheetName:
            previousRow = rows[j-1]
        else:
            previousRow = []
        nextRow = []
        if (j + 1) < len(rows):
            if rows[j+1][0].sheet_name == sheetName:
                nextRow = rows[j+1]
        oldSheetName = sheetName
        file = row[0].file
        corpus = row[0].corpus
        neighbors = collectNumberOfNeighbors(previousRow, row, nextRow, -1)
        newRow = [createEmptyCell(emptyCellData, rowNumber, -1, neighbors, Strings.start_cell, file, sheetName, corpus)]
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
                    neighbors = collectNumberOfNeighbors(previousRow, row, nextRow, -1)
                    newRow.append(createEmptyCell(emptyCellData, rowNumber, i, neighbors, Strings.end_cell, file, sheetName, corpus))
            else:
                neighbors = collectNumberOfNeighbors(previousRow, row, nextRow, i)
                newRow.append(createEmptyCell(emptyCellData, rowNumber, i, neighbors, Strings.empty_cell, file, sheetName, corpus))
            i = i + 1
        newRows.append(newRow)
    return(newRows)

emptyCell = createEmptyCell(emptyCellData, 156, 157, 158, Strings.empty_cell, "abc", "def", "fgh")

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




