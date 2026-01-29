
import serial
import time
from serial.tools import list_ports

class serial_interface(object):
    """Class that reads data from Serial"""

    # data IDs. Coordinado con Arduino
#    PUENTE = [0,1,2,3,4,5]
    SONAR = 0
#    LORO_REC = 7
    TIMON = 1
    ARPEGIATOR = 2
    MIC_BUTTON = 3
    SERES_ISLA = [4, 5, 6, 7, 8, 9]
    SLIDE_RIBBON = [10, 11]
    CUEVA_SEL = [12, 13, 14]
    SW = [15, 16, 17, 18, 19, 20]
    POT = [21, 22]
    SELVA_ONE_SHOT = [23, 24, 25, 26, 27, 28]
    SELVA_SEL = [29, 30, 31, 32]
    JOY_X = 33
    JOY_Y = 34
    BPM = 35
    TEMPO = 36 
    INDEX = 37
    DATA = 38 # Serial.availableForWrite
    N = 39      # num of data items

    def open_port(self) :
        self.serial_port = serial.Serial()
#        self.serial_port.baudrate = 9600
        self.serial_port.baudrate = 115200
#        print(str(serial.tools.list_ports())) No funciona
        n = len(serial.tools.list_ports.comports())
        print("n serial ports = " + str(n))
#        self.serial_port.port = 'COM10'
#        self.serial_port.port = 'COM5'
        try:
                self.serial_port.port = 'COM4'
                self.serial_port.open()
                self.serial_port.flushInput()
        except:
             print("Could not open serial port")

    def read_serial_data(self) :
#        self.serial_port.flush()
#        data = self.serial_port.readline().split().decode()
#        data = self.serial_port.readline().split()  # Este parece que funciona...
        data = self.serial_port.readline().decode()
        self.serial_port.write(b'<')
#        return str(data)
        return data


