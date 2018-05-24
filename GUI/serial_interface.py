
import serial
import time


class serial_interface(object):
    """Clas that reads data from Serial"""

    # data IDs
    PUENTE = [0,1,2,3,4,5]
    SONAR = 6
    LORO_REC = 7
    TIMON = 8
    ARPEGIATOR = 9
    SERES_SELVA = [10, 11, 12, 13, 14, 15]
    SLIDE_RIBBON = [16, 17]
    CUEVA_SEL = [18, 19, 20]
    SW = [21, 22, 23, 24, 25, 26]
    POT = [27, 28]
    SELVA_ONE_SHOT = [29, 30, 31, 32, 33, 34]
    SELVA_SEL = [35, 36, 37, 38]
    JOY_X = 39
    JOY_Y = 40
    BPM = 41
    TEMPO = 42
    DATA = 43

    def open_port(self) :
        self.serial_port = serial.Serial()
#        self.serial_port.baudrate = 9600
        self.serial_port.baudrate = 115200
#        self.serial_port.port = 'COM5'
#        print(str(serial.tools.list_ports()))
        self.serial_port.port = 'COM10'
        self.serial_port.open()
        self.serial_port.flushInput()

    def read_serial_data(self) :
#        self.serial_port.flush()
        data = self.serial_port.readline().split()
        self.serial_port.write(b'<');
        return str(data)


