from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from functools import partial

class configWindow(QWidget):
    update_config = pyqtSignal()

    @classmethod
    def isFrame(cls,frame):
        try:
            for key in frame:
                if isinstance(frame[key],dict):
                    if not cls.isFrame(frame[key]): return False
                elif isinstance(frame[key],str): pass
                elif isinstance(frame[key],list):
                    for n in frame[key]:
                        if not isinstance(n,str):return False
                else: return False
        except:return False
        return True
    
    
    
    
    def __init__(self,config,frame=None):
        super().__init__()

        self.config = config
        self.frame = frame
        self.widgets = {}
        self.windows = {}
        if self.frame is None:
            layout=self.launchFromDefault()
        elif self.isFrame(self.frame):
            layout=self.launchFromFrame()
        else:
            raise UserWarning("Frame of incorrect shape proceding with Default")

        self.setLayout(layout)
    


    def launchFromFrame(self,config = None):
        
        if config is None: config = self.config
        layout = QVBoxLayout()
        for key in self.frame:
            if isinstance(self.frame[key],dict):
                layout.addLayout(self.dictWidget(key))

            elif isinstance(self.frame[key],list):
                layout.addLayout(self.comboWidget(key,self.frame[key],config[key]))
            else:
                match self.frame[key]:
                    case "bool":
                        layout.addWidget(self.boolWidget(key,config[key]))
                    case "int":
                        layout.addLayout(self.intWidget(key,config[key]))
                    case "float":
                        layout.addLayout(self.intWidget(key,config[key]))
                    case "str":
                        layout.addLayout(self.strWidget(key,config[key]))

                    case _:
                        pass
        return layout



    def launchFromDefault(self,config = None):
        if config is None: config = self.config
        layout = QVBoxLayout()
        for key in config:
            if isinstance(config[key],dict):
                layout.addLayout(self.dictWidget(key))
            elif isinstance(config[key],bool):layout.addWidget(self.boolWidget(key,config[key]))
            elif isinstance(config[key],int):layout.addLayout(self.intWidget(key,config[key]))
            elif isinstance(config[key],float):layout.addLayout(self.floatWidget(key,config[key]))
            elif isinstance(config[key],str):layout.addLayout(self.strWidget(key,config[key]))
            else:
                layout.addLayout(self.staticWidget(key,config[key]))
        return layout
    

    def boolWidget(self,title,value):
        label = QCheckBox(title)
        label.setChecked(value)
        label.stateChanged.connect(partial(self.save_config,title,"bool"))
        self.widgets[title]=label

        return label

    def strWidget(self,title,value):
        
        label = QLabel(title)
        edit = QLineEdit(value)
        edit.editingFinished.connect(partial(self.save_config,title,"str"))
        self.widgets[title]=edit

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        return layout

    def intWidget(self,title,value):
        label = QLabel(title)
        edit = QLineEdit(str(value))
        edit.editingFinished.connect(partial(self.save_config,title,"int"))
        self.widgets[title]=edit

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        return layout

    def floatWidget(self,title,value):
        label = QLabel(title)
        edit = QLineEdit(str(value))
        edit.editingFinished.connect(partial(self.save_config,title,"float"))
        self.widgets[title]=edit

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        return layout

    def comboWidget(self,title,options,value):
        
        label = QLabel(title)
        edit = QComboBox()
        edit.addItems(options)
        
        try:
            value = options.index(value)
            edit.setCurrentIndex(value)
        except ValueError:
            pass
        
        edit.currentTextChanged.connect(partial(self.save_config,title,"combo"))
        self.widgets[title]=edit

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        return layout

    def dictWidget(self,title):
        label = QLabel(title)
        button = QPushButton("config")
        button.pressed.connect(partial(self.subDictDisplay,title))
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        return layout

    def subDictDisplay(self,title):
        if title in self.windows:self.windows[title].close()
        if self.frame is None:
            self.windows[title]=configWindow(self.config[title])
        elif self.isFrame(self.frame):
            self.windows[title]=configWindow(self.config[title],frame=self.frame[title])
        
        self.windows[title].show()
    
    def staticWidget(self,title,value):
        label = QLabel(title)
        edit = QLineEdit(str(value))
        edit.setEnabled(False)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        return layout
    
    def save_config(self,key,w_type):
        match w_type:
            case "bool": 
                value=self.widgets[key].checkState()
                if value == Qt.CheckState.Checked: value = True
                else: value = False
            case "str":
                value=self.widgets[key].text()
            case "int":
                value=self.widgets[key].text()
                try: value = int(value)
                except:
                    print("Can't cast to int. Reverting")
                    value = self.config[key]
                    self.widgets[key].setText(str(value))

            case "float": 
                value=self.widgets[key].text()
                try: value = float(value)
                except:
                    print("Can't cast to float. Reverting")
                    value = self.config[key]
                    self.widgets[key].setText(str(value))
            case "combo":
                value=self.widgets[key].currentText()
            case _:
                value = self.config[key]
        
        self.config[key]=value
        
        self.config[key]

    def closeEvent(self, a0):
        for wind in self.windows.values():
            wind.close()
        self.update_config.emit()
        return super().closeEvent(a0)
    
