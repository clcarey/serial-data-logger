import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

import sys

from configWindow import configWindow
from serialConnection import SerialConnection
from fileManagement import saveFile
from dataCollectThread import dataThread
 
class ComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


class MainWindow (QMainWindow):

    def __init__(self,configW):
        super().__init__()
        self.configW=configW
        #TODO Add default values class variables
        #self.initUI() #waits for signal to initiate the UI

    @pyqtSlot()
    def recieveConfig(self):
        [self.serial_baud_rate,self.channel_num,self.data_title,self.plot_num,self.plot_axis]=self.configW.get_config()
        self.sc = SerialConnection(self.serial_baud_rate)
        self.initUI()
        self.show()
        
    def initUI(self):
        
        self.setWindowTitle("Data Logger")

        self.serial_select_label = QLabel("Select Serial Port")#TODO filter out not real port info
        self.serial_select = ComboBox()
        self.generate_serial_options()
        self.serial_select.popupAboutToBeShown.connect(self.generate_serial_options)

        self.connect_serial_button = QPushButton("Connect Serial",self)
        self.connect_serial_button.clicked.connect(self.connect_Serial)
        
        self.disconnect_serial_button = QPushButton("Disconnect",self)
        self.disconnect_serial_button.clicked.connect(self.disconnect_Serial)

        self.serial_write_label = QLabel("Serial Write")
        self.ser_write = QLineEdit("")
        self.ser_write.textEdited.connect(self.serial_write)
        
        self.set_savefilename = QLabel("Save File Name")
        self.savefilename = QLineEdit("filename")          #TODO: auto iterate filename to help with overwriting
        
        self.launch_button = QPushButton("Begin Data Collection")
        self.launch_button.setCheckable(True)
        self.launch_button.clicked.connect(self.data_Collection)

        
        self.testgraph = pg.PlotWidget()
        self.testgraph.setBackground("w")
        self.testgraph.resize(400,300)
        
        
        
        #create layout for Config dialog
        layout = QVBoxLayout()
        layout.addWidget(self.serial_select_label)
        layout.addWidget(self.serial_select)
        layout.addWidget(self.connect_serial_button)
        layout.addWidget(self.disconnect_serial_button)
        layout.addWidget(self.serial_write_label)
        layout.addWidget(self.ser_write)
        layout.addWidget(self.set_savefilename)
        layout.addWidget(self.savefilename)
        #layout.addWidget()
        layout.addWidget(self.launch_button)
        
        super_layout = QHBoxLayout()
        super_layout.addLayout(layout)
        super_layout.addWidget(self.testgraph)
        
        
        widget = QWidget()
        widget.setLayout(super_layout)
        self.setCentralWidget(widget)
        #self.resize(400,300)

    def generate_serial_options(self):
        self.serial_select.clear()
        self.serial_ports = self.sc.list_serial()
        self.serial_select.addItems(self.serial_ports)
    
    def connect_Serial(self):
        self.sc.set_port(self.serial_select.currentText())
        self.sc.connect()
    def disconnect_Serial(self):
        self.sc.disconnect()
        
    def serial_write(self):
        self.sc.send_char(self.ser_write.text())
        self.ser_write.clear()
        
    def data_Collection(self,checked):
        time = [1,2,3,4,5,6,7]
        yaxis = [2,4,6,7,7.5,8,8.25]
        self.testgraph.plot(time,yaxis)
        
        
        if checked:
            #create savefile with header
            self.sf = saveFile()
            self.sf.set_filename(self.savefilename.text(),'.csv')
            self.sf.create_header(self.data_title)
            #start data collection
            self.dataThread = dataThread(self.sc,self.sf)
            self.dataThread.start()
            
        else:
            #When unclicked, safely stop thread
            self.dataThread.stopstop()
            self.dataThread.quit()

        



