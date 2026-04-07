import serial

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyqtgraph as pg

from data_channel import DataChannel
import sys


class dataThread(QThread):
    #running = False
    new_dat=pyqtSignal()
    data_start = pyqtSignal()

    def __init__(self,serial_connection,file_save,data_config):
        super().__init__()
        self.ser = serial_connection
        self.sf = file_save
        self.saving = False
        self.expectedDat = len(data_config)

        self.data_channels = []

        for item in data_config:
            self.data_channels.append(DataChannel.channel_from_dict(data_config[item]))
        
        #data check
        self.dataChecking = False
        self.dataCheckInd = 0
        self.lastCheck = 0
    
    
    def save_instance(self):
        for i,channel in enumerate(self.data_channels):
            channel.new(self.data[i])
        self.data = []
        for channel in self.data_channels:
            self.data.append(channel.last_read)
            if channel.config["parse"]["active"]:
                self.data.append(channel.parsed_read)
        
    def plot(self):
        self.new_dat.emit()

    def run(self):
        self.ser.ser.reset_input_buffer()
        self.ser.ser.readline()
        self.running = True

        while self.running:
            #read serial
            if self.ser.ser.in_waiting > 0:
                temp = self.ser.ser.readline()
                try:self.data=temp.decode()
                except:print("decode failed")
                self.data = self.data.split(',')

                if len(self.data) == self.expectedDat:
                    self.save_instance()
                    self.plot()
            
            #save data
                    if self.saving:
                        self.sf.write_row(self.data)
                else:
                    print("Unexpected data:")
                    print(self.data)

            
    def set_fileName(self,new_value):
        self.sf = new_value

    def set_Data(self,new_value):
        self.saving = new_value

    def stopSerial(self):
        self.running = False
