# Serial Data Logger

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Example](#Example)

## About <a name = "about"></a>
This Data logger is designed to interface cleanly with serial based communication to microcontrollers or similar, and allow for easy data viewing and saving to file. This serial viewer assumes the incoming data is printed in a csv format and will save to a csv format of the user specified name. There is capability to input parameters for data saving (data headers, number of plots and content, serial baud rate etc.) or a simple configuration .txt file can be interpretted by the script.
Also of note, and absent in many other similar applications available, is the simulteneous ability to _send_ characters/communication to the microcontroller during data collection.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

This code is largely python, utilizing PyQT5 for the UI elements. Most the necessary modules come in standard python packages, but the requirements file should include all the used modules needed for functionality.
Modules Used:
```
PyQt5
pyserial
pyqtgraph
python-csv
TIME-python
os-sys
```

### Installing

Install Python

Install prerequisite libraries:
```
pip install requirements.txt
```

### Configuration File
The code allows for a configuration file to be used to streamline data collection. The code will read a .txt file and identify serial baud rate, data titles, and plot axises from lines beginning with '#' followed by a four character identifier. The line after is read as the value (or next two lines for plot). Anything outside of this will be dismissed as a comment.
Codes:
```
#Seri - Serial Baud rate
#Data - Data Title
#Plot - Add Plot with axises
```
For example the following snippet will take a serial communicication containing "[timevalue],[position value]" and plot position with respect to time in 1 plot:
```
This is a comment
#Serial Baud rate:
9600
#Data channel 1:
Time (ms)
#Data channel 2:
Position (m)

#Plot
0
1
```

## Example
Included in the example folder is a basic prebuilt microcontroller script that demonstrates the serial communication with some basic data. 
