import json

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyqtgraph as pg

import sys

from .serialConnection import SerialConnection,serial_frame 
from .configWindow import configWindow
from .fileManagement import saveFile
from .dataManagementThread import dataThread
 
class ComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


class MainWindow (QMainWindow):

    def __init__(self,setupW):
        super().__init__()
        self.setupW=setupW
        self.config_winds = {}
        self.sf = saveFile()



    @pyqtSlot()
    def recieveConfig(self):
  
        self.config=self.setupW.get_config()
        try:
            self.sc = SerialConnection(self.config["serial"])
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
        except KeyError as e:
            print("Bad Config: closing app")
            print(e)
            self.setupW.close()
            self.close()
            
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

        self.serial_config_button = QPushButton("Serial Settings",self)
        self.serial_config_button.clicked.connect(self.show_serial_config)

        self.serial_write_label = QLabel("Serial Write")
        self.ser_write = QLineEdit("")
        self.ser_write.textEdited.connect(self.serial_write)
        
        self.set_savefilename = QLabel("Save File Name")
        self.savefilename = QLineEdit(self.config["savefile"])
        self.savefilename.editingFinished.connect(self.set_savename)
        
        self.launch_button = QPushButton("Begin Data Collection")
        self.launch_button.setCheckable(True)
        self.launch_button.clicked.connect(self.data_Collection)

        self.save_config_button = QPushButton("save config to file")
        self.save_config_button.clicked.connect(self.save_config)

        self.plots_list = []
        for i in range (self.config["plotting"]["plot num"]):
            self.plots_list.append(pg.PlotWidget())
            self.plots_list[i].setBackground("w")
        
        
        #create layout for Config dialog
        layout = QVBoxLayout()
        layout.addWidget(self.serial_select_label)
        layout.addWidget(self.serial_select)
        layout.addWidget(self.connect_serial_button)
        layout.addWidget(self.disconnect_serial_button)
        layout.addWidget(self.serial_config_button)
        layout.addWidget(self.serial_write_label)
        layout.addWidget(self.ser_write)
        layout.addWidget(self.set_savefilename)
        layout.addWidget(self.savefilename)
        layout.addWidget(self.launch_button)
        layout.addWidget(self.save_config_button)
        
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
        if not (self.sc.ser is None):
            self.dataThread.start()

    def disconnect_Serial(self):
        self.dataThread.stopSerial()
        self.sc.disconnect()
        
    def serial_write(self):
        self.sc.send_char(self.ser_write.text())
        self.ser_write.clear()
    
    def show_serial_config(self):
        self.config_winds["serial"] = configWindow(self.config["serial"],frame=serial_frame)
        self.config_winds["serial"].show()

    @pyqtSlot()
    def plotData(self):
        for plot in self.plots_list:plot.clear() 
        for channel in self.dataThread.data_channels:
            if channel.config["plotting"]["active"]:
                #print(channel.buffer)
                try:
                    self.plots_list[channel.config["plotting"]["plot num"]-1].plot(channel.x_ref,channel.buffer,label = channel.config["plotting"]["name"])
                except:
                    channel.clear_buffer()
                    print("Plotting error clearing buffer")

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

    def save_config(self):
        
        name = QFileDialog.getSaveFileName(self,"Configuration Save File")
        if name[0][-5:]==".json":config_path = name[0]
        else: config_path = name[0]+".json"
        with open(config_path,'w') as jsonfile:
            json.dump(self.config,jsonfile,indent=4)
            
        

    def closeEvent(self, a0):
        for wind in self.config_winds.values():
            wind.close()
        self.setupW.close()
        return super().closeEvent(a0)
