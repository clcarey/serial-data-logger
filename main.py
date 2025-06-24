import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

from configWindow import configWindow
from serialConnection import SerialConnection
from dataWindow import MainWindow



app = QApplication(sys.argv)

configWind = configWindow()
dataWind = MainWindow(configWind)

configWind.readySignal.connect(dataWind.recieveConfig)



#dataWind.show()
configWind.show()
app.exec_()
