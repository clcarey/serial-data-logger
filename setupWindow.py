import serial
import copy

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from configWindow import configWindow
from serialConnection import default_config as serial_default_config
from data_channel import default_config as data_default_config
from serialConnection import serial_frame
from data_channel import data_frame

import sys
import json

class setupWindow (QMainWindow):
    readySignal=pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.winds = {}
        self.config = {
            "serial" : serial_default_config.copy(),
            "channel num": 0,
            "plotting":{
                "plot num": 0,
            },
            "savefile": "./data/filename",
            "data" : {}
            }
        self.initUI()
        self.config_flag = False
        
    def initUI(self):    
        self.setWindowTitle("Config")
        
        self.select_config_button = QPushButton("Select Config File",self)
        self.select_config_button.clicked.connect(self.openFileDialog)
        
        self.manual_config_label = QLabel("Manual Configuration:")

        self.serial_setup = QPushButton("Serial Settings")
        self.serial_setup.clicked.connect(self.show_serial)
        
        self.data_num_label = QLabel("Enter Data number:")
        self.data_num_line = QLineEdit(str(self.config["channel num"]))
        self.data_num_line.editingFinished.connect(self.update_data_num)
        
        data_num_layout = QHBoxLayout()
        data_num_layout.addWidget(self.data_num_label)
        data_num_layout.addWidget(self.data_num_line)

        self.graph_num_label = QLabel("Plot number:")
        self.graph_num_line = QLineEdit(str(self.config["plotting"]["plot num"]))
        self.graph_num_line.editingFinished.connect(self.update_graph_num)
        
        graph_num_layout = QHBoxLayout()
        graph_num_layout.addWidget(self.graph_num_label)
        graph_num_layout.addWidget(self.graph_num_line)

        self.data_setup = QPushButton("Configure Data Channels")
        self.data_setup.clicked.connect(self.show_data)

        self.launch_button = QPushButton("Launch Manual Configuration")
        self.launch_button.clicked.connect(self.launch_data)
        #self.launch_button.setEnabled(False)
        
        #create layout for Config dialog
        layout = QVBoxLayout()
        layout.addWidget(self.select_config_button)
        layout.addWidget(self.manual_config_label)
        layout.addWidget(self.serial_setup)
        layout.addLayout(data_num_layout)
        layout.addLayout(graph_num_layout)
        layout.addWidget(self.data_setup)
        layout.addWidget(self.launch_button)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_serial(self):
        self.winds["serial"]=configWindow(self.config["serial"],frame=serial_frame)
        self.winds["serial"].show()

    def show_data(self):
        self.config["data"]=self.generate_data_config()
        frame = self.generate_data_frame()
        self.winds["data"]=configWindow(self.config["data"],frame=frame)
        self.winds["data"].show()

    def generate_data_config(self):
        data_dict = {}
        for channel in range(self.config["channel num"]):
            data_dict["Channel "+str(channel)]=copy.deepcopy(data_default_config)
        return data_dict

    def generate_data_frame(self):
        frame_dict = {}
        template = copy.deepcopy(data_frame)
        plot_options = []
        for n in range(self.config["plotting"]["plot num"]):
            plot_options.append(str(n+1))
        template["plotting"]["plot num"]=plot_options
        for channel in range(self.config["channel num"]):
            frame_dict["Channel "+str(channel)]=template
        return frame_dict


    def update_data_num(self):
        value=self.data_num_line.text()
        try: value = int(value)
        except:
            print("Can't cast to int. Reverting")
            value = self.config["channel num"]
            self.data_num_line.setText(str(value))
        self.config["channel num"]= value


    def update_graph_num(self):
        value=self.graph_num_line.text()
        try: value = int(value)
        except:
            print("Can't cast to int. Reverting")
            value = self.config["plotting"]["plot num"]
            self.data_num_line.setText(str(value))
        self.config["plotting"]["plot num"]= value

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
        self.readySignal.emit()    
        self.hide()

