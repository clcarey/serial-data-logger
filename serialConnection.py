import serial
import serial.tools.list_ports

#PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
#STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
#FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)


class SerialConnection():
    def __init__(self,serial_baudrate):
        # Initialize serial connection settings
        self.serial_baudrate = serial_baudrate
        self.port_select = ""        
        self.ser = None

    def connect(self,**kwargs):
        try:
            # Attempt to establish the serial connection
            self.serial_port = self.port_select #reads serial port selected from dropdown select
            self.ser = serial.Serial(self.serial_port, self.serial_baudrate, timeout = 1,**kwargs)
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
