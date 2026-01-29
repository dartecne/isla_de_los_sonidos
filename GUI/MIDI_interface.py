import mido
import mido.backends.rtmidi
import rtmidi
import logging


class MIDI_interface(object):
    """send MIDI messages"""

    def connect(self):
        print( "IN:" + str(mido.get_input_names()) )
        print( "OUT:" + str(mido.get_output_names()) )
        n = len( mido.get_output_names() )
        midi_port = mido.open_output(mido.get_output_names()[n-1])

        self.outport = midi_port
        return midi_port
#
#        self.outport = mido.open_output("isla 2")
#        self.outport = mido.open_output()

    def get_input_names(self):
        return( mido.get_input_names() )

    def get_output_names(self):
        return( mido.get_output_names() )

    def test_note_on(self):
        msg = mido.Message( 'note_on', channel = 3, note=60, velocity=127 );
        self.outport.send(msg)
        logging.debug( "test_note_on" )

    def note_on(self, note, vel, channel = 1):
        msg = mido.Message( 'note_on', channel = channel - 1, note=note, velocity=vel );
        self.outport.send(msg)
        logging.debug( "note_on: " + str(channel) + ", "+ str(note) + ", "+ str(vel) )

    def note_off(self, note, vel, channel = 1):
        msg = mido.Message( 'note_off', channel = channel - 1, note=note, velocity=vel );
        self.outport.send(msg)
        logging.debug( "note_off: " + str(channel) + ", "+ str(note) + ", "+ str(vel) )

    def control_change(self, control, value, channel = 1 ):
        msg = mido.Message( 'control_change', channel = channel-1, control=control, value=value );
        self.outport.send(msg)
   #     logging.debug( "CC: " + str(channel) + ", "+ str(control) + ", "+ str(value) )

#   Input is string in the form C#-4, Db-4, or F-3. If your implementation doesn't use the hyphen, 
#   just replace the line :
#    letter = midstr.split('-')[0].upper()
#   with:
#    letter = midstr[:-1]

    def MidiStringToInt(self, midstr):
        Notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
        answer = 0
        i = 0
        #Note
        letter = midstr.split('-')[0].upper()
        for note in Notes:
            for form in note:
                if letter.upper() == form:
                    answer = i
                    break;
            i += 1
        #Octave
        answer += (int(midstr[-1]))*12
        return answer
