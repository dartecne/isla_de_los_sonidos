import mido
from python_osc import dispatcher
from python_osc import osc_server

MIDI_PORT_NAME = 'OSC-Python-Out'

# 1. Intentar abrir el puerto MIDI
try:
    # En Windows con loopMIDI, open_output suele funcionar directo si el puerto existe.
    outport = mido.open_output(MIDI_PORT_NAME)
    print("Puerto MIDI Abierto: {}".format(MIDI_PORT_NAME))
except Exception as e:
    print("Error al abrir puerto MIDI: {}".format(e))
    print("Lista de puertos disponibles:", mido.get_output_names())
    exit()

OSC_IP = "192.168.1.3" # Asegurate que esta es la IP de LISA (Windows 7)
OSC_PORT = 8000

def control_volume_handler(address, *args):
    """
    Maneja el mensaje OSC y lo convierte a MIDI
    """
    if not args:
        return
        
    osc_value = args[0] # El valor float entre 0.0 y 1.0
    
    # Convertirpyt a rango MIDI (0-127)
    midi_value = int(osc_value * 127)
    # Asegurar que no se salga del rango por errores de redondeo
    midi_value = max(0, min(127, midi_value))

    print("OSC: {} = {:.2f} -> MIDI: {}".format(address, osc_value, midi_value))

    # Crear mensaje MIDI (CC 7 es Volumen)
    cc_number = 7
    midi_message = mido.Message(
        'control_change',
        channel=0, 
        control=cc_number,
        value=midi_value
    )

    outport.send(midi_message)

# 2. Configurar el Dispatcher (esto faltaba en tu codigo original)
disp = dispatcher.Dispatcher()
disp.map("/fader/volumen", control_volume_handler)

# 3. Iniciar servidor
print("\nIniciando Servidor OSC en {}:{}".format(OSC_IP, OSC_PORT))
server = osc_server.BlockingOSCUDPServer((OSC_IP, OSC_PORT), disp)

try:
    server.serve_forever()  
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
    server.server_close()
    outport.close()