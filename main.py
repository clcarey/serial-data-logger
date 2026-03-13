import serial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

from configWindow import configWindow
from serialConnection import SerialConnection
from dataWindow import MainWindow
from wakepy import keep


app = QApplication(sys.argv)

configWind = configWindow()
dataWind = MainWindow(configWind)

configWind.readySignal.connect(dataWind.recieveConfig)

configWind.show()
with keep.presenting():
#dataWind.show()
    app.exec_()
