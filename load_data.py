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
        self.row_number = get_row_number(self.cell_adress)
        self.column_number = get_column_number(self.cell_adress)
        self.sheet = self.file + self.sheet_name

def isFirstSheet(data):
    return(data[0] == "michelle_lokay__26590__IGSUpdate.xls" and data[2] == "Sheet1")


def getSheetPosition(cells, sheet_name):
    for i in range(0, len(cells)):
        if cells[i][0].sheet == sheet_name:
            return i
    return None

def parseCsvFile():
    with open('49_features_downsampled_dataset.csv') as csvfile:
        datareader = csv.reader(csvfile, delimiter = ',', quotechar = '\'')
        sheets = []
        last_sheet = ""
        sheet_position = -1
        for row in datareader:
            cell = Cell(row)
            sheet_position = getSheetPosition(sheets, cell.sheet)
            if (sheet_position is None):
                sheets.append([cell])
            else:
                sheets[sheet_position].insert(get_cell_position(sheets[sheet_position], cell), cell)
    #Testing:
    
    print(len(sheets))
    print(len(sheets[0]))
    print(len(sheets[1]))


    outputs = set()

    for sheet in sheets:
        output = set()
        for cell in sheet:
            output.add(cell.sheet)
        if len(output) != 1:
            print(output)
        outputs.add(output.pop())
    print(len(outputs))
    #for cell in cells[0]:
        #print(cell.sheet)
    return(sheets)

