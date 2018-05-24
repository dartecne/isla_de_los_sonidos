import mido
import mido.backends.rtmidi

import time


def test_note_on():
    print( "Test MIDI noteOn" )
    msg = mido.Message( 'note_on', note=60 );
    print(msg)
    outport.send(msg)

def test_control_change():
    print( "Test MIDI control change" )
    for i in range(127):
        msg = mido.Message( 'control_change', control=12, value=i );
        outport.send(msg)
        time.sleep(0.200)

print(mido.get_input_names())
print(mido.get_output_names())
outport = mido.open_output()
print( "MIDI port opened:" + str(outport) )
test_note_on()
time.sleep( 3 )
test_control_change()
time.sleep( 3 )

