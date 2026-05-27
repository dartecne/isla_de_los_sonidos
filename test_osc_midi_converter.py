import socket
import struct
import ctypes
from ctypes import wintypes

# Cargar la libreria de Windows para MIDI
winmm = ctypes.windll.winmm

# Configuracion MIDI
MIDI_PORT_NAME = 'isla'

# Funciones de Windows MIDI API
def find_midi_port(port_name):
    """Busca un puerto MIDI por nombre"""
    num_devices = winmm.midiOutGetNumDevs()
    
    class MIDIOUTCAPS(ctypes.Structure):
        _fields_ = [
            ("wMid", wintypes.WORD),
            ("wPid", wintypes.WORD),
            ("vDriverVersion", wintypes.DWORD),
            ("szPname", wintypes.WCHAR * 32),
            ("wTechnology", wintypes.WORD),
            ("wVoices", wintypes.WORD),
            ("wNotes", wintypes.WORD),
            ("wChannelMask", wintypes.WORD),
            ("dwSupport", wintypes.DWORD)
        ]
    
    for device_id in range(num_devices):
        caps = MIDIOUTCAPS()
        result = winmm.midiOutGetDevCapsW(device_id, ctypes.byref(caps), ctypes.sizeof(caps))
        if result == 0:
            if port_name.lower() in caps.szPname.lower():
                return device_id
    return None

# Buscar puerto MIDI
print("Buscando puerto MIDI '{}'...".format(MIDI_PORT_NAME))
device_id = find_midi_port(MIDI_PORT_NAME)

if device_id is None:
    print("\nERROR: No se encontro el puerto '{}'".format(MIDI_PORT_NAME))
    print("Asegurate de que loopMIDI este abierto.\n")
    print("Puertos disponibles:")
    num_devices = winmm.midiOutGetNumDevs()
    for i in range(num_devices):
        caps = ctypes.create_string_buffer(256)
        winmm.midiOutGetDevCapsA(i, caps, 256)
        print("  - {}".format(caps.value.decode('latin-1', errors='ignore')))
    exit(1)

# Abrir puerto MIDI
hmidiout = wintypes.HANDLE()
result = winmm.midiOutOpen(
    ctypes.byref(hmidiout),
    device_id,
    0, 0, 0
)

if result != 0:
    print("ERROR: No se pudo abrir el puerto MIDI (codigo {})".format(result))
    exit(1)

print("Puerto MIDI abierto correctamente: {}".format(MIDI_PORT_NAME))

def send_midi_cc(channel, control, value):
    """Envia un mensaje MIDI Control Change"""
    # Formato: Status byte + Control + Value
    # Status = 0xB0 + channel (0xB0 = Control Change)
    status = 0xB0 | (channel & 0x0F)
    message = status | (control << 8) | (value << 16)
    winmm.midiOutShortMsg(hmidiout, message)

# Configuracion OSC
OSC_IP = "0.0.0.0"
OSC_PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((OSC_IP, OSC_PORT))
sock.settimeout(0.5)

print("\nServidor OSC escuchando en {}:{}".format(OSC_IP, OSC_PORT))
print("Esperando mensajes ...")
print("Presiona Ctrl+C para salir\n")

def parse_osc_string(data, offset):
    """Extrae cadena OSC"""
    end = data.index(b'\x00', offset)
    string = data[offset:end].decode('ascii')
    next_offset = ((end + 4) // 4) * 4
    return string, next_offset

def parse_osc_float(data, offset):
    """Extrae float Big Endian"""
    value = struct.unpack('>f', data[offset:offset+4])[0]
    return value, offset + 4

def parse_osc_int(data, offset):
    """Extrae int Big Endian"""
    value = struct.unpack('>i', data[offset:offset+4])[0]
    return value, offset + 4

# Loop principal
try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue 
            
        try:
            osc_address, offset = parse_osc_string(data, 0)
            type_tags, offset = parse_osc_string(data, offset)
            print(data)
            
#            if osc_address == "/sensor/force/id3" and type_tags.startswith(",f"):
            if osc_address == "/bridge/id3/force" :
                osc_value, offset = parse_osc_int(data, offset)
                
                # Convertir a MIDI
                midi_value = int(osc_value * 127)
                midi_value = max(0, min(127, midi_value))
                print("OSC: {:.3f} -> MIDI CC23 = {}".format(osc_value, midi_value))
                
                # Enviar MIDI CC23 (Volumen) en canal 0
                send_midi_cc(0, 23, midi_value)
            
        except Exception as e:
            print("Error: {}".format(e))

except KeyboardInterrupt:
    print("\n\nCerrando...")
    winmm.midiOutClose(hmidiout)
    sock.close()
    print("Adios!")
