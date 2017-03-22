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

def getEmptyCell(emptyCellData, rowNumber, columnNumber, label, sheetName):
    emptyCellData[49] = label
    emptyCellData[24] = rowNumber
    emptyCellData[25] = columnNumber
    emptyCellData[2] = sheetName
    emptyCellData[5] = "(" + str(columnNumber) + "," + str(rowNumber) + ")"
    return(Cell(emptyCellData))




emptyCell = getEmptyCell(emptyCellData, 2,2, "empty", "abc")

print("Empty cell features:" + str(emptyCell.features) + "; length = " + str(len(emptyCell.features)))

rows = parseCsvFile()
print("Length of longest row" + str(getHighestColumnNumber(rows)))
print("Full cell features:" + str(rows[0][0].features) + "; length = " + str(len(rows[0][0].features)))

