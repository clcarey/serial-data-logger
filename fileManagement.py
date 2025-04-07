import csv


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
        self.data_expected = len(column_names)
        with open(self.full_fileName,'w',newline='') as logFile:
            logWriter = csv.writer(logFile)
            logWriter.writerow(column_names)

    def write_row(self, data):
        with open(self.full_fileName,'a',newline='') as logFile:
            logWriter = csv.writer(logFile)
            logWriter.writerow(data)

    def attach_plot(self):
        pass
