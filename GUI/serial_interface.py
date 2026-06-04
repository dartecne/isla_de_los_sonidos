
import serial
import time
from serial.tools import list_ports
#from elements_ids import *

class serial_interface(object):
    """Class that reads data from Serial"""

    def open_serial_port(self) :
        self.serial_port = serial.Serial()
#        self.serial_port.baudrate = 9600
        self.serial_port.baudrate = 115200
        sp = serial.tools.list_ports.comports()
        n = len( sp )
        print( sp[n-1] ) 
        print( "n serial ports = " + str(n) )
        try:
                self.serial_port.port = 'COM6'
                self.serial_port.open()
                self.serial_port.flushInput()
                return self.serial_port
        except:
                print("Could not open serial port")
                return None

    def read_serial_data(self) :
#        self.serial_port.flush()
#        data = self.serial_port.readline().split().decode()
#        data = self.serial_port.readline().split()  # Este parece que funciona...
        data = self.serial_port.readline().decode()
        print(data)
        self.serial_port.write(b'<')
#        return str(data)
        return data


