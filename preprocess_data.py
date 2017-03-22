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

def createEmptyCell(emptyCellData, rowNumber, columnNumber, label, file, sheetName):
    emptyCellData[49] = label
    emptyCellData[24] = rowNumber
    emptyCellData[25] = columnNumber
    emptyCellData[0] = file
    emptyCellData[2] = sheetName
    emptyCellData[5] = "(" + str(columnNumber) + "," + str(rowNumber) + ")"
    return(Cell(emptyCellData, label))

def padRows(rows, maxLength):
    newRows = []
    for row in rows:
        rowNumber = row[0].row_number
        sheetName = row[0].sheet_name
        file = row[0].file
        newRow = [createEmptyCell(emptyCellData, rowNumber, -1, Strings.start_cell, file, sheetName)]
        oldIndex = 0
        nextCell = row[oldIndex]
        for i in range(0, maxLength + 1):
            if nextCell.column_number == i:
                newRow.append(nextCell)
                oldIndex = oldIndex + 1
                if oldIndex < len(row):
                    nextCell = row[oldIndex]
            else:
                newRow.append(createEmptyCell(emptyCellData, rowNumber, i, Strings.empty_cell, file, sheetName))
                
        newRow.append(createEmptyCell(emptyCellData, rowNumber, maxLength + 1, Strings.end_cell, file, sheetName))
        newRows.append(newRow)
    return(newRows)


emptyCell = createEmptyCell(emptyCellData, 2,2, Strings.empty_cell, "abc", "def")

print("Empty cell features:" + str(emptyCell.features) + "; length = " + str(len(emptyCell.features)))

rows = parseCsvFile()
maxLength = getHighestColumnNumber(rows)
print("Length of longest row" + str(maxLength))
print("Full cell features:" + str(rows[0][0].features) + "; length = " + str(len(rows[0][0].features)))

paddedRows = padRows(rows, maxLength)


