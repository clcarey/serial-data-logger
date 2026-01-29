from enum import Enum
import time

class Errors(Enum):
    UNEXPECTED_VALUE = 1 
    RANGE_ERROR_HIGH = 2
    RANGE_ERROR_LOW = 4
    BAD_PARSE = 8
    BAD_RANGE = 16

class ParseType(Enum):
    SINGLE_START = 0
    SINGLE_END = 1
    SINGLE_SPLIT = 2
    MULTI_START = 3
    MULTI_END = 4
    MULTI_SPLIT = 5

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


    def new(self,value,x_new=time.time()):
        self.last_read = value
        temp = self.last_read
        if self.config["parse"]["active"]: 
            self._parse()
            temp = self.parsed_read
        if self.config["range"]["active"]: self.check_range()

        if not self._error and self.config["plotting"]["active"]:
            self.x_ref.append(x_new)
            self.buffer.append(temp)
            if len(self.buffer)>self.config["plotting"]["buffersize"]:
                self.x_ref.pop(0)
                self.buffer.pop(0)
            
        self.check_error()
    
    #%% Parsing
    #TODO: integrate a more robust parsing library
    def _parse(self):
        match self.config["parse"]["type"]:
            case ParseType.SINGLE_START.value: self.parsed_read = self.single_start_parse(self.last_read)
            case ParseType.SINGLE_END.value: self.parsed_read = self.single_end_parse(self.last_read)
            case ParseType.SINGLE_SPLIT.value: self.parsed_read = self.single_split_parse(self.last_read)
            case ParseType.MULTI_START.value: self.parsed_read = self.multi_start_parse(self.last_read)
            case ParseType.MULTI_END.value: self.parsed_read = self.multi_end_parse(self.last_read)
            case ParseType.MULTI_SPLIT.value: self.parsed_read = self.multi_split_parse(self.last_read)
            case _:
                print("default case reached") 
                self.parsed_read = self.last_read
                self._error |= Errors.BAD_PARSE.value

    def single_split_parse(self,value):
        try:
            temp = value.split(self.config["parse"]["start"])
            parsed_value = temp[len(temp)-1]
        except:
            self._error |= Errors.BAD_PARSE.value
            return value
        try:
            temp = parsed_value.split(self.config["parse"]["stop"])
            parsed_value = temp[0]
        except:
            self._error |= Errors.BAD_PARSE.value

        return parsed_value
    
    def single_start_parse(self,value):
        print("Parser not yet integrated")
        return value

    def single_stop_parse(self,value):
        print("Parser not yet integrated")
        return value

    def multi_start_parse(self,value):
        print("Parser not yet integrated")
        return value

    def multi_stop_parse(self,value):
        print("Parser not yet integrated")
        return value

    def multi_split_parse(self,value):
        print("Parser not yet integrated")
        return value    

    def check_range(self):
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

    def clear_error(self):
        self._error = 0b00

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