import csv


class CsvParser:
    def __init__(self):
        self.filename = 'data.csv'

    def readCsv(self):
        f = open(self.filename, 'r', encoding='UTF-8')
        rdr = csv.reader(f)
        data = []
        for line in rdr:
            data.append([line[0], line[1]])
        f.close()
        return data

    def appendCsv(self, path, pid):
        f = open(self.filename, 'a', encoding='UTF-8', newline='')
        wr = csv.writer(f)
        wr.writerow([path, pid])
        f.close()

    def removeCsv(self, path, pid):
        data = self.readCsv()
        data.remove([path, pid])
        f = open(self.filename, 'w', encoding='UTF-8', newline='')
        wr = csv.writer(f)
        for line in data:
            wr.writerow(line)
        f.close()

    def writeCsv(self):
        f = open(self.filename, 'w', encoding='UTF-8', newline='')
        f.close()