import serial

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from serialConnection import default_config as serial_default_config
import sys
import json

class setupWindow (QMainWindow):
    readySignal=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

        self.config = {
            "serial" : serial_default_config.copy(),
            "plotting":{
                "plot num": 1
            },
            "savefile": "./data/filename",
            "data" : {}
            }
        
        self.config_flag = False
        
    def initUI(self):    
        self.setWindowTitle("Config")
        
        self.select_config_button = QPushButton("Select Config File",self)
        self.select_config_button.clicked.connect(self.openFileDialog)
        
        self.DEV_MESSAGE = QLabel("UNDER MAINTENENCE")

        self.serial_set_label = QLabel("Enter Serial Baud Rate:")
        self.serial_line = QLineEdit()
        #self.serial_line.isEnabled(False)
        
        self.data_num_label = QLabel("Enter Data number:")
        self.data_num_line = QLineEdit()
        #self.data_num_line.isEnabled(False)

        self.data_names_label = QLabel("Comma Separated Data Names:")
        self.data_names_line = QLineEdit()
        #self.data_names_line.isEnabled(False)

        self.graph_num_label = QLabel("Enter graph number:")
        self.graph_num_line = QLineEdit()
        #self.graph_num_line.isEnabled(False)

        self.graph_axis_label = QLabel("Enter graph axis:")
        self.graph_axis_line = QLineEdit("xaxis1,yaxis1,xaxis2,yetc")
        #self.graph_axis_line.isEnabled(False)

        self.launch_button = QPushButton("Manual entry under dev use file")
        self.launch_button.clicked.connect(self.launch_data)
        self.launch_button.setEnabled(False)
        
        #create layout for Config dialog
        layout = QVBoxLayout()
        layout.addWidget(self.select_config_button)
        layout.addWidget(self.DEV_MESSAGE)
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
        try:
            with open(file) as json_file:
                self.config = json.load(json_file)
            self.config_flag = True
        except:
            print("Couldn't read. json expected. Try Again")

    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.read_config_file(selected_files[0])
            
        if self.config_flag:
            self.readySignal.emit()
            self.hide()
            
    def get_config(self):
        return self.config

    def launch_data(self):
        self.serial_baud_rate = int(self.serial_line.text())        
        self.channel_num = int(self.data_num_line.text())
        self.plot_num = int(self.graph_num_line.text())
        self.data_title = self.data_names_line.text()
        self.plot_axis = self.graph_axis_line.text()
        self.readySignal.emit()    
        self.hide()

