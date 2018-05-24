

import serial
import time


class serial_interface(object):
    """Clas that reads data from Serial"""
    seq = []
    n_line = 1
    def open_port(self) :
        self.serial_port = serial.Serial()
#        self.serial_port.baudrate = 9600
        self.serial_port.baudrate = 115200
#        self.serial_port.port = 'COM10'
        self.serial_port.port = 'COM5'
        self.serial_port.timeout = None
        self.serial_port.rts = True
        self.serial_port.dtr = True
        self.serial_port.open()
        self.serial_port.flushInput()
        settings = self.serial_port.getSettingsDict()
        print(settings)

    def read_line(self) :
        data = self.serial_port.readline().split()
        self.serial_port.write(b'<');
        return data

    def read_serial_data_append(self) :
        data = [];
        while(True):
            d = self.serial_port.readline().split()
#            print(d)
            if( d==[b'>'] ) : break
            data.append(d);
        self.serial_port.write(b'<');
        return data
            

#        self.serial_port.flushInput()
#        values = data.decode().split(',')
        return data

    def read_serial_char(self):
#        data = self.serial_port.read(self.serial_port.inWaiting())
        n_data = 0
        while True :
            c = self.serial_port.read(1)
            self.seq.append( c.decode('utf-8') )
            data = ''.join(str(v) for v in self.seq)
            n_data += 1
            print( "c = " + c.decode('utf-8') + " seq = " + str(self.seq) + "data = " + data + "n = " + str(n_data))
            if c.decode() == '\n':
#            if c == 10:
                print( "Line " + str(self.n_line) + ': ' + '[' + str(n_data) + ']: ' + data)
                self.seq = []
                self.n_line += 1
                break
                return data

if __name__ == '__main__':
    myserial = serial_interface()
    myserial.open_port()
    while True:
#        data = myserial.read_serial_char()
        data = myserial.read_line()
        print (data)
#        print (len(data))
#        print (data.split(","))
