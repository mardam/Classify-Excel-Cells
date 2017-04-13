import csv

def saveData(rows):
    with open('prepared_data.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            for cell in row:
                writer.writerow(cell.features + [cell.label])
