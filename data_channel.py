from enum import Enum
import time

class Errors(Enum):
    UNEXPECTED_VALUE = 1 
    RANGE_ERROR_HIGH = 2
    RANGE_ERROR_LOW = 4
    BAD_PARSE = 8
    BAD_RANGE = 16

class ParseType(Enum):
    SCALE_PARSE = 0
    PARSE_1 = 1
    PARSE_2 = 2
    PARSE_3 = 3
    PARSE_4 = 4
    PARSE_5 = 5

default_config = { 
        "plotting": {
            "active": False,
            "name" : "",
            "color" : "",
            "linestyle" : "",
            "buffersize": 50,
            },
        "range" : {
            "active": False,
            "high": None,
            "low" : None
            },
        "parse" : {
            "active":False,
            "type" : None,
            "start": None,
            "end" : None
            }
        }   


class DataChannel():
    """
    A class for the storage and management of Data Streams in data collection systems.

    Attributes:
        config (dict): Configuration of Data channel
            plotting (dict):
                active (bool): Plotting occuring
                name (str): Name associated with data for legends
                plot num (int): indicator of plot to associate data with
                buffersize (int): number of points to store and plot
            range (dict):
                active (bool): Check data is in range
                low (float): Low Reference
                high (float): High Reference
            parse (dict):
                active (bool): Parse input str typically for plotting
                type (int): select between parse types
        last_read (str): last added data point
        parsed_read (str): (if active) parse of last_read
        buffer (arr): stored array of specified length of reads
        x_ref (arr): mirror array to buffer containing elapsed time by default or an additional unit
        
    Methods:
        channel_from_dict: create a new instance from a configuration dictionary
        new: Add a new data point

    """
    @classmethod
    def channel_from_dict(cls,config_dict):
        obj = cls()
        obj.config = config_dict
        obj._init()
        return obj


    def _init(self):
        self.last_read = None
        self.parsed_read = None
        self.buffer=[]
        self.x_ref = []
        self._error = 0b0


    def new(self,value,x_new= None,x_start = time.time()):
        
        if x_new is None:x_new = time.time() - x_start
        self.last_read = value
        temp = self.last_read
        if self.config["parse"]["active"]:
            #This will remove any r and n
            self.last_read=self.last_read.rstrip("\\rn")
            self._parse()
            temp = self.parsed_read
        if self.config["range"]["active"]: self.check_range()

        if not self._error and self.config["plotting"]["active"]:
            self.x_ref.append(x_new)
            self.buffer.append(float(temp))
            if len(self.buffer)>self.config["plotting"]["buffersize"]:
                self.x_ref.pop(0)
                self.buffer.pop(0)
            
        self.check_error()
    
    #%% Parsing
    #TODO: integrate a more robust parsing library
    def _parse(self):
        self.clear_error(Errors.BAD_PARSE)
        match self.config["parse"]["type"]:
            case ParseType.SCALE_PARSE.value: self.parsed_read = self.parse0(self.last_read)
            case ParseType.PARSE_1.value: self.parsed_read = self.parse1(self.last_read)
            case ParseType.PARSE_2.value: self.parsed_read = self.parse2(self.last_read)
            case ParseType.PARSE_3.value: self.parsed_read = self.parse3(self.last_read)
            case ParseType.PARSE_4.value: self.parsed_read = self.parse4(self.last_read)
            case ParseType.PARSE_5.value: self.parsed_read = self.parse5(self.last_read)
            case _:
                print("default case reached") 
                self.parsed_read = self.last_read
                self._error |= Errors.BAD_PARSE.value

    def parse0(self,value):
        #parse for scales: expects data to be of the format "+/- XXXX kg"
        try:
            parsed_value = value.replace(" ","")
        except:
            self._error |= Errors.BAD_PARSE.value
            return value
        try:
            temp = parsed_value.split("k")
            if len(temp) == 1: raise Exception("no starting parse found")
            parsed_value = temp[0]
        except:
            self._error |= Errors.BAD_PARSE.value
        return parsed_value
    
    def parse1(self,value):
        print("Parser not yet integrated")
        return value

    def parse2(self,value):
        print("Parser not yet integrated")
        return value

    def parse3(self,value):
        print("Parser not yet integrated")
        return value

    def parse4(self,value):
        print("Parser not yet integrated")
        return value

    def parse5(self,value):

        print("Parser not yet integrated")
        return value    

    def check_range(self):
        self.clear_error(Errors.BAD_RANGE.value)  
        try:
            if self.config["parse"]["active"]:
                if float(self.parsed_read) < self.config["range"]["low"]: self._error |= Errors.RANGE_ERROR_LOW.value
                elif float(self.parsed_read) > self.config["range"]["high"]: self._error |= Errors.RANGE_ERROR_HIGH.value
            else:
                if float(self.last_read) < self.config["range"]["low"]: self._error |= Errors.RANGE_ERROR_LOW.value
                elif float(self.last_read) > self.config["range"]["high"]: self._error |= Errors.RANGE_ERROR_HIGH.value
        except:
            self._error |= Errors.BAD_RANGE.value

    def check_error(self):
        if self._error:
            error_code = bin(self._error)[2:]
            for i,n in enumerate(error_code):
                    if int(n):
                        print(Errors(2**(len(error_code)-(i+1))).name)
                        #raise(Errors(n))

    def clear_error(self,bit = None):
        if bit == None:
            self._error = 0b00
        elif isinstance(bit,Errors):
            temp = 0b11111
            temp ^= bit.value
            self._error &= temp

    @property
    def range(self):
        return [self.config["range"]["low"],self.config["range"]["high"]]
    
    @range.setter
    def range(self,new):
        try:
            self.config["range"]["active"] = True
            self.config["range"]["low"] = new[0]
            self.config["range"]["high"] = new[1]
        except:
            raise("BAD RANGE GIVEN")
    @range.deleter
    def range(self):
        self.config["range"]["active"] = False
        self.config["range"]["low"] = None
        self.config["range"]["high"] = None
    
    @property
    def parse(self):
        return [self.config["parse"]["active"],self.config["parse"]["start"],self.config["parse"]["stop"]]
    
    @parse.setter
    def parse(self,new):
        try: 
            self.config["parse"]["type"] = 2
            self.config["parse"]["active"]=True
            start = new[0]
            stop = new[1]
            self.config["parse"]["start"] = start
            self.config["parse"]["stop"] = stop
        except:
            raise("BAD PARSE GIVEN")
        
    @parse.deleter
    def parse(self):
        self.config["parse"]["active"] = False
        self.config["parse"]["start"] = None
        self.config["parse"]["stop"] = None

    def clear_buffer(self):
        self.buffer = []
        self.x_ref = []
"""
        def new(self,value):
            self.last_read = value
            if self.Plotting:
                self.plotting_details["buffer"].append(value)
                if len(self.plotting_details["buffer"])>self.plotting_details["buffersize"]:
                    self.plotting_details["buffer"].pop(0)
            #error_check()


        #check for various errors
        def error_check(self):
            if self.error.bit_count():
                for i,n in enumerate(bin(self.error)[2:]):
                    if int(n):
                        raise(self.error_list[i])
        #print(n)

            else: 
                print("No error :)")

            #if self.last_read


        #Toggle plotting
        #Deciding on how to approach plotting info here: do I require it as an input for turning it on (I don't think so)
        #do I run a check to make sure it's valid 
        #where do I send the value if it's not valid (error probably)
        def set_plotting(self):
            pass

        #Set expected range for data channel, which will inform the error checker
        def set_range(self):
            pass
"""