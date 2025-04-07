import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class dataThread(QThread):
    running = False
    def __init__(self,serial_connection,file_save):
        super().__init__()
        self.ser = serial_connection
        self.sf = file_save
    

    def run(self):
        self.ser.ser.reset_input_buffer()
        self.running = True
        while self.running:
            #read serial
            data = []
            if self.ser.ser.in_waiting > 0:            
                data=self.ser.ser.readline().decode()
                data = data.split(',')
            #save data
                self.sf.write_row(data)
        
        
        

    def stopstop(self):
        self.running = False
