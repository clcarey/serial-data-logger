import csv
import os
import time

class saveFile():
    def __init__(self):
        self.filename = "blank"
        self.file_ext = ".csv"
        self.full_fileName = self.filename + self.file_ext
        
    def set_filename(self,name,ext = ".csv"):
        self.filename = name
        self.file_ext = ext
        self.full_fileName = self.filename + self.file_ext

    def get_filename(self):
        self.full_fileName = self.filename + self.file_ext
        return self.full_fileName

    def create_header(self,column_names):
        ind = 1        
        while self.check_file():
            self.full_fileName = self.filename + str(ind) + self.file_ext
            ind = ind + 1
        self.data_expected = len(column_names)
        writecolumn = [str("UTC")]
        writecolumn.extend(column_names)
        with open(self.full_fileName,'w',newline='') as logFile:
            logWriter = csv.writer(logFile)
            logWriter.writerow(writecolumn)

    def write_row(self, data):
        with open(self.full_fileName,'a',newline='') as logFile:
            logWriter = csv.writer(logFile)
            writedata = [str(time.time())]
            writedata.extend(data)
            logWriter.writerow(writedata)
    
    def check_file(self):
        return os.path.isfile(self.full_fileName)

    def attach_plot(self):
        pass
