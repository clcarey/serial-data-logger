import serial
import serial.tools.list_ports

#PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
#STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
#FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

serial_frame = {
    "baud rate": "int",
    "parity": ["None","Even","Odd","Mark","Space"],
    "stop bit":["1","1.5","2"],
    "bits":["5","6","7","8"],
    "timeout":"int"
}
default_config = {
        "baud rate": 9600,
        "parity": "None",
        "stop bit":"1",
        "bits":"8",
        "timeout": 1
}


class SerialConnection():
    def __init__(self,serial_config):

        if self.check_config(serial_config):self.config=serial_config
        else: self.config = default_config.copy()

        self.port_select = ""        
        self.ser = None

    def check_config(self,config):
        for key in default_config:
            if not (key in config):return False
        return True
        

    def connect(self):
        try:
            # Attempt to establish the serial connection
            self.serial_port = self.port_select #reads serial port selected from dropdown select
            serial.Serial()

            match self.config["parity"]:
                case "None":parity = 'N'
                case "Even":parity = 'E'
                case "Odd": parity = 'O'
                case "Mark":parity = 'M'
                case "Space":parity = 'S'
                case _:pass
            match self.config["stop bit"]:
                case "1":stopbit=1
                case "1.5":stopbit=1.5
                case "2":stopbit=2
                case _:pass
            match self.config["bits"]:
                case "5":bits=5
                case "6":bits=6
                case "7":bits=7
                case "8":bits=8
                case _:pass


            self.ser = serial.Serial(self.serial_port,
                                     baudrate=self.config["baud rate"],
                                     parity=parity,
                                     stopbits=stopbit,
                                     bytesize=bits,
                                     timeout=self.config["timeout"])
                                      
            print("Serial connection established.")
            self.ser.flush()
        except serial.SerialException as e:
            print("Error: Serial connection failed -", e)

    def disconnect(self):
        try:
            self.ser.close()
            print("Serial connection closed.")
        except:
            print("Serial connection failed to close")

    def set_port(self,port):
        self.port_select= port

    def list_serial(self):
        #looks up what serial ports exist and returns them
        port_return =[] #'/dev/ttys002'
        self.serial_ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(self.serial_ports):
            port_return.append(port)
        return port_return
        
    def send_char(self,message):
        self.ser.write(message.encode())
