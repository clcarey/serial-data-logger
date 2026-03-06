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
pip install -r requirements.txt
```

### Configuration File
The code allows for a configuration file to be used to streamline data collection. The code will read a .json file and identify serial baud rate, data titles, and plot axises
The file "gui_config_helper.py" is a terminal based script that will generate the appropriate file, or alternatively the format should look as follows:
```
{
    "serial_baud_rate": 9600,
    "channel_num": 2,
    "plot_num": 1,
    "filename":"filename",
    "data": {
        "Channel 1": {
            "plotting": {
                "active": false,
                "name": null,
                "plot num": null,
                "color": "r",
                "linestyle": "",
                "buffersize": null
            },
            "range": {
                "active": false,
                "low": null,
                "high": null
            },
            "parse": {
                "active": false,
                "type": null,
                "start": null,
                "stop": null
            }
        },
        "Channel 2": {...}
    }
}
```

## Example
Included in the example folder is a basic prebuilt microcontroller script that demonstrates the serial communication with some basic data. 
(Example is not yet updated for lastest release)
