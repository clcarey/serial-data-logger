# Serial Data Logger

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Example](#Example)

## About <a name = "about"></a>
This Data logger is designed to interface cleanly with serial based communication to microcontrollers or similar, and allow for easy data viewing and saving to file. This serial viewer assumes the incoming data is printed in a csv format and will save to a csv format of the user specified name. There is capability to input parameters for data saving (data headers, number of plots and content, serial parameters etc.) or a configuration file can be interpretted by the script.
Also of note, and absent in many other similar applications available, is the simulteneous ability to _send_ characters/communication to the microcontroller during data collection.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

This code is largely python, utilizing PyQT6 for the UI elements. Most the necessary modules come in standard python packages, but the requirements file should include all the used modules needed for functionality.
Modules Used:
```
PyQt6
pyserial
pyqtgraph
wakepy
```

### Installing

Install Python

Download serial-data-logger to directory of choice.

Install prerequisite libraries:
pipenv is recommended for this project for a deterministic build, but a requirement.txt file is also provided.
The terminal commands in the directory of the project:
```
pipenv install
```
_or_

```
pip install -r requirements.txt
```
### Configuration File
The code allows for a configuration file to be used to streamline data collection. The code will read a .json file and identify serial, data channel information and plotting information.
An existing configuration can be saved from the main gui window.
A new file can be generated with "gui_config_helper.py," a terminal based script that will generate the appropriate file or alternatively the format should look as follows:
```
{

    "serial": {"baud rate":9600,
            "parity": "None",
            "stop bit":"1",
            "bits":"8",
            "timeout": 1
            }

    "channel num": 2,
    "plot num": 1,
    "filename":"filename",
    "data": {
        "Channel 1": {
            "plotting": {
                "active": false,
                "name": null,
                "plot num": null,
                "color": "r",
                "linestyle": "",
                "buffersize": null,
                "displaytime": 3600
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
## Other Features

### Parse
Within the configuration settings you will notice a "parse" sub directory. This is a tool meant to allow for built-in management of less than perfect data. To plot in real time data must be castable to int or float, some data channels may not be set up where this is natively possible, for example scale interfaces often include the unit: +XXX.X _kg_, to read the kg must be removed. 

A couple parse methods are built-in:
- SCALE_PARSE : Built for the above case 
- STRIP_SLASHN : Removes extra \\n from data line (often present at the end of a dataline)
- PARSE_2 : Alternative scale method for g instead of kg
- PARSE_3 : Unallocated
- PARSE_4 : Unallocated
- PARSE_5 : Unallocated

Unallocated parse methods are set-up for ease of development for user if unique needs exist for them, code for this should be written in data_channel.py.

At the point of saving any parsed channel will report 2 values, the raw data read from serial, and the parsed value, so that no data is lost to bad parses.

### More in progress ->
Some upcoming features in development are data health metrics. Including checking the channels against a set healthy range and indicating to the user, and checking for anomolies in the data (not reading channel etc).

Additional configuration features will be added soon, allowing for more flexibility on a runnning instance of the main GUI. Data configuration, and addition/removal of channels and reordering of channels. And finally addition/removal of plots.


## Example
Included in the example folder is a basic prebuilt microcontroller script that demonstrates the serial communication with some basic data.
