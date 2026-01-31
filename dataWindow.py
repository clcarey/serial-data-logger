import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

import sys

from configWindow import configWindow
from serialConnection import SerialConnection
from fileManagement import saveFile
from dataManagementThread import dataThread
 
class ComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


class MainWindow (QMainWindow):

    def __init__(self,configW):
        super().__init__()
        self.configW=configW
        self.sf = saveFile()

        #TODO Add default values class variables


    @pyqtSlot()
    def recieveConfig(self):
        self.config=self.configW.get_config()

        self.sc = SerialConnection(self.config["serial_baud_rate"])

        col_names = []
        for n in self.config["data"]:
            col_names.append(n)
            if self.config["data"][n]["parse"]["active"]:
                col_names.append(n + "- parsed")
        self.sf.set_columnNames(col_names)

        self.dataThread = dataThread(self.sc,self.sf,self.config["data"])
        self.dataThread.new_dat.connect(self.plotData)
        
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
        self.savefilename = QLineEdit(self.config["filename"])
        self.savefilename.editingFinished.connect(self.set_savename)
        
        self.launch_button = QPushButton("Begin Data Collection")
        self.launch_button.setCheckable(True)
        self.launch_button.clicked.connect(self.data_Collection)


        self.plots_list = []
        for i in range (self.config["plot_num"]):
            self.plots_list.append(pg.PlotWidget())
            self.plots_list[i].setBackground("w")
        
        
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
        layout.addWidget(self.launch_button)
        
        super_layout = QHBoxLayout()
        super_layout.addLayout(layout)
        for plot in self.plots_list:
            super_layout.addWidget(plot)
        
        
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
        #for i,plots in enumerate(self.plots_list):
        #    self.dataThread.attach_plot(self.plot_axis[2*i],self.plot_axis[2*i+1])
            

        self.sc.connect()
        self.dataThread.start()

    def disconnect_Serial(self):
        self.dataThread.stopSerial()
        self.sc.disconnect()
        
    def serial_write(self):
        self.sc.send_char(self.ser_write.text())
        self.ser_write.clear()
        
    
    @pyqtSlot()
    def plotData(self):
        for plot in self.plots_list:plot.clear() 
        for channel in self.dataThread.data_channels:
            if channel.config["plotting"]["active"]:
                #print(channel.buffer)
                self.plots_list[channel.config["plotting"]["plot num"]-1].plot(channel.x_ref,channel.buffer,label = channel.config["plotting"]["name"])
 

    def set_savename(self):
        self.sf.set_filename(self.savefilename.text(),'.csv')

    def data_Collection(self,checked):
        
        if checked:
            #create savefile with header
            self.sf.set_filename(self.savefilename.text(),'.csv')
            #start data collection
            self.dataThread.set_Data(True)
            
        else:
            #When unclicked, safely stop thread
            self.dataThread.set_Data(False)
            self.sf.set_active(False)
            #self.dataThread.quit()