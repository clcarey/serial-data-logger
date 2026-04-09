import serial

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import sys

from serialDataLogger import setupWindow,MainWindow
from wakepy import keep


app = QApplication(sys.argv)

setupWind = setupWindow()
dataWind = MainWindow(setupWind)

setupWind.readySignal.connect(dataWind.recieveConfig)

setupWind.show()
with open("resources/stylesheet.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

with keep.presenting():
#dataWind.show()
    app.exec()
