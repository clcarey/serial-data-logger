import serial
import serial.tools.list_ports

class SerialConnection():
    def __init__(self,serial_baudrate):
        # Initialize serial connection settings
        self.serial_baudrate = serial_baudrate
        self.port_select = ""        
        self.ser = None

    def connect(self):
        try:
            # Attempt to establish the serial connection
            self.serial_port = self.port_select #reads serial port selected from dropdown select
            self.ser = serial.Serial(self.serial_port, self.serial_baudrate, timeout = 1)
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
