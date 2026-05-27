import mido
from python_osc.osc_server import BlockingOSCUDPServer, dispatcher

MIDI_PORT_NAME = 'OSC-Python-Out'

try:
    outport = mido.open_output(MIDI_PORT_NAME)
    print("Puerto MIDI Abierto: {}".format(MIDI_PORT_NAME))
except Exception as e:
    print("Error al abrir puerto MIDI. ¿Está loopMIDI abierto? Error: {}".format(e))
    exit()

#OSC_IP = "192.168.1.6"
OSC_IP = "0.0.0.0"
OSC_PORT = 8000

def control_volume_handler(address, *args):
    """
    Maneja el mensaje OSC de /fader/volumen y lo convierte a MIDI Control Change (CC)
    """
    osc_value = args[0]

midi_max = 127
midi_value = int(osc_value * midi_max)
print("OSC recibido: {} = {:.2f} -> MIDI Valor: {}".format(address, osc_value, midi_value))

cc_number = 7

midi_message = mido.Message(
    'control_change',
    channel=cc_number,
    value=midi_value
)

outport.send(midi_message)
print("-> Enviado: CC {} con valor {}".format(cc_number, midi_value))

disp.map("/force/id4", control_volume_handler)
print("\nIniciando Servidor OSC en {}:{}".format(OSC_IP, OSC_PORT))
server = BlockingOSCUDPServer((OSC_IP, OSC_PORT), disp)

try:
    server.serve_forever()  
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
    server.server_close()
    outport.server_close()
    outport.close()
    