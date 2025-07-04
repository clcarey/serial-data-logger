import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

import sys


class dataThread(QThread):
    #running = False
    new_dat=pyqtSignal()
    data_start = pyqtSignal()

    def __init__(self,serial_connection,file_save,channel_num):
        super().__init__()
        self.ser = serial_connection
        self.sf = file_save
        self.saving = False
        self.expectedDat = channel_num
        
        #plotting stuff
        self.data = []
        self.x_index = []
        self.y_index = []
        self.storedDatX = []
        self.storedDatY = []
        self.dataLen = 51

        #data check
        self.dataChecking = False
        self.dataCheckInd = 0
        self.lastCheck = 0

    def attach_plot(self,x_index,y_index):
        self.x_index.append(x_index)
        self.y_index.append(y_index)
        self.storedDatX.append([])
        self.storedDatY.append([])
    
    def attach_dataCheck(self,ind):
        self.dataChecking = True
        self.dataCheckInd = ind
    
    def save_instance(self):
        for i,channel in enumerate(self.storedDatX):
            if len(channel) > self.dataLen:
                self.storedDatX[i].pop(0)
            self.storedDatX[i].append(float(self.data[self.x_index[i]]))

        
        for i,channel in enumerate(self.storedDatY):
            if len(channel) > self.dataLen:
                self.storedDatY[i].pop(0)
            self.storedDatY[i].append(float(self.data[self.y_index[i]]))

    def plot(self):
        self.new_dat.emit()
        #for i,plots in enumerate(self.plots):
        #    plots.plot(self.storedDatX[i],self.storedDatY[i])

    def dataCheck(self):
        if self.lastCheck != self.data[self.dataCheckInd]:
            self.saving = True
        #print(self.data)
        self.lastCheck = self.data[self.dataCheckInd]

    def run(self):
        self.ser.ser.reset_input_buffer()
        self.running = True

        while self.running:
            #read serial
            if self.ser.ser.in_waiting > 0:            
                self.data=self.ser.ser.readline().decode()
                self.data = self.data.split(',')
                
                if self.dataChecking:
                    self.dataCheck()
                if len(self.data) == self.expectedDat:
                    self.save_instance()
                    self.plot()

                
            #save data
                    if self.saving:
                        self.sf.write_row(self.data)
                else:
                    print("Unexpected data:")
                    print(self.data)

            
    def set_fileName(self,new_value0):
        self.sf = new_value

    def set_Data(self,new_value):
        self.saving = new_value

    def stopSerial(self):
        self.running = False
