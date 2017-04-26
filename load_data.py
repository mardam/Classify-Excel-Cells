import csv
import re
import Strings
import warnings
import config

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

def parseNumberOfNeighbors(data):
    for i in range(26,31):
        if data[i] == "t":
            return(i - 26)
    raise("Cell " + data[5] + " has no number of Neighbors")

def parseFeatures(data, kind):
    #numberOfNeighbors = parseNumberOfNeighbors(data)
    data = data[6:config.row_number_position] + data[config.after_coordinates_position:151]
    features = []
    for elem in data:
        numValue = dataelement_to_float(elem)
        if numValue is not None:
            features.append(numValue)
    #features.append(numberOfNeighbors)
    if kind == Strings.empty_cell:
        return(features + [1,0,0])  
    if kind == Strings.start_cell:
        return(features + [0,1,0])
    if kind == Strings.end_cell:
        return(features + [0,0,1])
    return(features + [0,0,0])      # cell_type: empty, start, end

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
    def __init__(self, data, kind):
        self.label = data[config.label_position]
        self.features = parseFeatures(data, kind)
        self.file = data[config.file_name_position]
        self.corpus = data[config.corpus_name_position]
        self.sheet_name = data[config.sheet_name_position]
        self.cell_adress = data[config.cell_adress_position]
        self.row_number = int(data[config.row_number_position])#get_row_number(self.cell_adress)
        self.column_number = int(data[config.column_number_position])#get_column_number(self.cell_adress)
        self.row = self.file + self.sheet_name + str(self.row_number)
        
    def hasImportantClass(self):
        return(self.label in Strings.importantClasses)

    def setNeighbors(self, neighbors):
        self.features[len(self.features) - 4] = neighbors


def getRowPosition(cells, row_name):
    for i in range(0, len(cells)):
        if cells[i][0].row == row_name:
            return i
    return None

def parseCsvFile():
    with open('all_features_downsampled_dataset_binarized_remove_useless.csv') as csvfile:
        datareader = csv.reader(csvfile, delimiter = ',', quotechar = '\'')
        rows = []
        for dataCell in datareader:
            cell = Cell(dataCell, None)
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

def saveData(rows):
    with open('prepared_data.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            for cell in row:
                writer.writerow(cell.features + [cell.label])
