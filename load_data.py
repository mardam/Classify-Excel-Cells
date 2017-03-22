import csv
import re

def isFloat(elem):
    if re.match("^\d+?\.\d+?$", elem) is None:
        return False
    return True

def dataelement_to_float(elem):
    if elem.isnumeric():
        return(int(elem))
    if isFloat(elem):
        return(float(elem))
    if elem == "f":
        return(0)
    if elem == "t":
        return(1)
    return(None)

def parseFeatures(data):
    ret = []
    for elem in data:
        numValue = dataelement_to_float(elem)
        if numValue is not None:
            ret.append(numValue)
    return(ret)

def get_row_number(position):
    try:
        return int(re.search(r'\d+', position).group())
    except:
        print(position)
        raise("Error")

def get_column_number(position):
    column_string = re.search(r'[A-Z]+', position).group()
    length = len(column_string)
    return (length - 1) * 26 + ord(column_string[length - 1]) - 64

def get_cell_position(cells, cell):
    if len(cells) == 0:
        return (0)
    for i in range(0, len(cells)):
        if (cells[i].row_number > cell.row_number or (cells[i].row_number == cell.row_number and cells[i].column_number > cell.column_number)):
            return(i)
    return(len(cells))
                

class Cell(object):
    def __init__(self, data):
        self.label = data[49]
        self.features = parseFeatures(data)
        self.file = data[0]
        self.sheet_name = data[2]
        self.cell_adress = data[5]
        self.row_number = int(data[24])#get_row_number(self.cell_adress)
        self.column_number = int(data[25])#get_column_number(self.cell_adress)
        self.row = self.file + self.sheet_name + str(self.row_number)

    def previousRow():
        return(self.file + self.sheet_name + str(self.rownumber - 1))

    def nextRow():
        return(self.file + self.sheet_name + str(self.rownumber + 1))


def getRowPosition(cells, row_name):
    for i in range(0, len(cells)):
        if cells[i][0].row == row_name:
            return i
    return None

def parseCsvFile():
    with open('49_features_downsampled_dataset.csv') as csvfile:
        datareader = csv.reader(csvfile, delimiter = ',', quotechar = '\'')
        rows = []
        for dataCell in datareader:
            cell = Cell(dataCell)
            row_position = getRowPosition(rows, cell.row)
            if (row_position is None):
                rows.append([cell])
            else:
                rows[row_position].insert(get_cell_position(rows[row_position], cell), cell)
    #Testing:
    
    print("Number of Rows: " + str(len(rows)))
    print("Length of first row " + str(len(rows[0])))
    print("Length of second row: " + str(len(rows[1])))


    outputs = set()

    for row in rows:
        output = set()
        for cell in row:
            output.add(cell.row)
        if len(output) != 1:
            print("Arrays with cells from more or less than 1 row")
            print(output)
        outputs.add(output.pop())
    print("Number of rows:" + str(len(outputs)))
    return(rows)

