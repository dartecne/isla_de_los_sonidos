import socket
import struct
import ctypes
from ctypes import wintypes

# Cargar la libreria de Windows para MIDI
winmm = ctypes.windll.winmm

# Configuracion OSC
OSC_IP = "0.0.0.0"
OSC_PORT = 8000


"""
Interface similar a serial_interface, pero que toma los datos que hay en la red LISA
Estos datos se envía por OSC/UDP
"""

class osc_interface(object):
    """Class that reads data from OSC/UDP"""

    def __init__(self):
            #dataIDs
        self.OSC_ADD = ["/bridge/id0/force",
        "/bridge/id1/force",
        "/bridge/id2/force",
        "/bridge/id3/force",
        "/bridge/id4/force",
        "/bridge/id5/force",
        "/lorito/movement",
        "/lorito/pitch",
        "/lorito/roll",
        "/lorito/pressure"]

        self.N_OSC_DATA = len(self.OSC_ADD)
        self.data_array = [0] * self.N_OSC_DATA
        self.sock = None
        try:
            self.open_osc_port()
        except:
            print("ERROR abriendo OSC")

        
    def open_osc_port(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((OSC_IP, OSC_PORT))
        self.sock.settimeout(0.5)
        print("OSC port opened!")

    def parse_osc_data(self):
        data, addr = self.read_osc_data()
        data_out=[]
        if data is None:
            return None

        data_dict =  self.parse_osc_bundle(data)
        return self.osc_dict_to_array(data_dict)


    def read_osc_data(self):
        try:
            data, addr = self.sock.recvfrom(1024)
#            print(data)
            return data, addr
        except socket.timeout:
            return None, None 

    def parse_osc_bundle(self, data):
        result = {}

        try:
            if not data.startswith(b'#bundle'):
                print("No bundle!")
                return result

            offset = 16  # saltar "#bundle" + timetag

            base_address = ""

            while offset < len(data):

                size, offset = self.parse_osc_int(data, offset)

                msg_end = offset + size

                osc_address, offset = self.parse_osc_string(data, offset)
                type_tags, offset = self.parse_osc_string(data, offset)

                value = None

                if 'i' in type_tags:
                    value, offset = self.parse_osc_int(data, offset)

                # mensaje raíz
                if osc_address.endswith('/'):
                    base_address = osc_address.rstrip('/')

                # mensaje relativo
                else:
                    full_address = base_address + osc_address
                    result[full_address] = value

                offset = msg_end

        except Exception as e:
            print(f"Error OSC: {e}")

        return result

    def osc_dict_to_array(self, osc_dict):
        """
        Convierte:
            {'/lorito/id0/pitch': 26, ...}

        en:
            [0,0,0,0,0,0,0,26,103,37]
        """

        data_out = [0] * self.N_OSC_DATA

        for i, address in enumerate(self.OSC_ADD):
            if address in osc_dict:
                data_out[i] = osc_dict[address]

        return data_out

    def parse_osc_string(self, data, offset):
        """Extrae cadena OSC"""
        end = data.index(b'\x00', offset)
        string = data[offset:end].decode('ascii')#('ascii')
        next_offset = end + 1#((end + 4) // 4) * 4
        while next_offset % 4 != 0:
            next_offset += 1
        return string, next_offset

    def parse_osc_float(self, data, offset):
        """Extrae float Big Endian"""
        value = struct.unpack('>f', data[offset:offset+4])[0]
        return value, offset + 4

    def parse_osc_int(self, data, offset):
        """Extrae int Big Endian"""
        value = struct.unpack('>i', data[offset:offset+4])[0]
        return value, offset + 4

    def close(self):
        self.log_file.close()
        self.sock.close()


if __name__ == '__main__':
    try:
        my_interface = osc_interface()
#        my_interface.open_port()
        while True:
            values = my_interface.parse_osc_data()
            print(values)

    except KeyboardInterrupt:
        print("\n\nCerrando...")
        my_interface.close()
        print("Adios!")
        