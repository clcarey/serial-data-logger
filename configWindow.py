import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class configWindow (QMainWindow):
    readySignal=pyqtSignal()    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):    
        self.setWindowTitle("Config")
        
        self.select_config_button = QPushButton("Select Config File",self)
        self.select_config_button.clicked.connect(self.openFileDialog)
        
        self.serial_set_label = QLabel("Enter Serial Baud Rate:")
        self.serial_line = QLineEdit()
        
        self.data_num_label = QLabel("Enter Data number:")
        self.data_num_line = QLineEdit()

        self.data_names_label = QLabel("Comma Separated Data Names:")
        self.data_names_line = QLineEdit()

        self.graph_num_label = QLabel("Enter graph number:")
        self.graph_num_line = QLineEdit()

        self.graph_axis_label = QLabel("Enter graph axis:")
        self.graph_axis_line = QLineEdit("xaxis1,yaxis1,xaxis2,yetc")

        self.launch_button = QPushButton("Launch Data collection")
        self.launch_button.clicked.connect(self.launch_data)
        
        #create layout for Config dialog
        layout = QVBoxLayout()
        layout.addWidget(self.select_config_button)
        layout.addWidget(self.serial_set_label)
        layout.addWidget(self.serial_line)
        layout.addWidget(self.data_num_label)
        layout.addWidget(self.data_num_line)
        layout.addWidget(self.data_names_label)
        layout.addWidget(self.data_names_line)
        layout.addWidget(self.graph_num_label)
        layout.addWidget(self.graph_num_line)
        layout.addWidget(self.graph_axis_label)
        layout.addWidget(self.graph_axis_line)
        layout.addWidget(self.launch_button)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def read_config_file(self,file):
        self.channel_num = 0
        self.plot_num = 0
        self.data_title = []
        self.plot_axis = []

        with open(file) as file:
            linelist = [line.rstrip() for line in file]
        linelist[:] = [x for x in linelist if x]
        for i,x in enumerate(linelist):
            if x[0] == "#":
                if x[1:5] == "Seri":
                    self.serial_baud_rate = int(linelist[i+1])
                if x[1:5] == "Data":
                    self.data_title.append(linelist[i+1])
                    self.channel_num +=1
                if x[1:5] == "plot":
                    self.plot_axis.append(linelist[i+1])
                    self.plot_num +=1
    
    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.read_config_file(selected_files[0])
            self.readySignal.emit()
            self.hide()
    def get_config(self):
        return [self.serial_baud_rate,self.channel_num,self.data_title,self.plot_num,self.plot_axis]

    def launch_data(self):
        self.serial_baud_rate = int(self.serial_line.text())        
        self.channel_num = int(self.data_num_line.text())
        self.plot_num = int(self.graph_num_line.text())
        self.data_title = self.data_names_line.text()
        self.plot_axis = self.graph_axis_line.text()
        self.readySignal.emit()    
        self.hide()

