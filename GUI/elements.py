import threading
import logging
import time
import random

from elements_ids import *
from serial_interface import *
from osc_interface import *

class Element( threading.Thread ):

    def __init__( self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def __init__( self, threadID, name, q, MIDI):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.MIDI = MIDI

    def set_queue( self, q ):
        self.q = q

    def set_MIDI( self, MIDI ):
        self.MIDI = MIDI

class StatesDiagram( Element ):
    FADE_OUT_CC = 25
    FADE_IN_CC = 26
    EXPLOTION_NOTE = 31
    STOP_NOTE = 38
    init = time.perf_counter()
#    def __init__(self, threadID, name, q, MIDI):
#        Element.__init__(self, threadID, name, q, MIDI)

    def run(self):
#        LAPSO = 10 * 60 # lapso for changing the state of the island
        LAPSO = 10  # lapso for changing the state of the island
        while(True):
            if(( time.perf_counter() - self.init ) > LAPSO):
                logging.debug( "EXPLOTION!!!!" )
                self.fade_all_out()
                self.MIDI.note_on( self.EXPLOTION_NOTE, 127, channel = 1 )
#                time.sleep(2*60)
                self.fade_all_in()
                self.init = time.perf_counter()

    def fade_all_out(self):
        self.MIDI.note_on( self.STOP_NOTE, 127, channel = 1 )
        for i in range(127):
            self.MIDI.control_change(  self.FADE_OUT_CC, i, channel = 1)
#            time.sleep(0.4)

    def fade_all_in(self):
        for i in range(127):
            self.MIDI.control_change(  self.FADE_IN_CC, i, channel = 1)
#            time.sleep(0.4)

class Secuenciador( Element ):
    d_old = 0
    d = 0
    arp_state = [0,0,0,0,0,0]
    seres_last_note = 0
    ambiente_last_note = 0

    def handle_lorito(self):
        #data[LORITO]: movement, pitch, roll, pressure
        #movement = [0, 100]
        #
        LORITO_ON_THRES = 60
        LORITO_OFF_THRES = 20
        if( self.data[LORITO[0]] != self.data_old[LORITO[0]] ):
            if(int(self.data[LORITO[0]]) > LORITO_ON_THRES ):
                self.MIDI.note_on(LORITO_NOTE, 127, 1 )
                logging.debug("LORITO_NOTE: " + str(self.data[LORITO[0]]) )

        if( self.data[LORITO[1]] != self.data_old[LORITO[1]] ):
#            v = self.normalize(int(self.data[LORITO[1]]), 0 , 128, 0, 127 )
            v = int(self.data[LORITO[1]]) 
            self.MIDI.control_change(LORITO_CC[0], v)
            logging.debug("LORITO_CC: " + str(v) )

        if( self.data[LORITO[2]] != self.data_old[LORITO[2]] ):
#            v = self.normalize(int(self.data[LORITO[1]]), 0 , 128, 0, 127 )
            v = int(self.data[LORITO[2]]) 
            self.MIDI.control_change(LORITO_CC[1], v)
            logging.debug("LORITO_CC: " + str(v) )

    def handle_tunel(self):
        SONAR_THRES = 80   #cm
        NOISE_THRES = 12

        if( int(self.data[SONAR]) > NOISE_THRES ) :
            self.d = int(self.data[SONAR] )
            logging.debug("SONAR: " + self.data[SONAR] )

        if( (self.d < SONAR_THRES ) &
            (self.d_old > SONAR_THRES)):
            self.MIDI.note_on( TUNEL_NOTE, 127, channel = 1 )

        self.d_old = self.d

    def handle_puente(self):
        #data[PUENTE] = [2100, 2900] sin peso
        #data[PUENTE] = [1500, 500] con peso

        PUENTE_ON_THRES = [2100, 2100, 2100, 2100, 2100, 2100] # menos de esto alguien pisa
        PUENTE_OFF_THRES = [1500, 1500, 1500, 1500, 1500, 1500] # más de esto alguien se levanta
        NOISE_FILTER = 50 # cambios permitidos de datos consecutivos en el tiempo

        for i in range(6):
#            d = int(self.data[PUENTE_FORCE[i]]) - int(self.data_old[PUENTE[i]])
#            d = abs(d)
#            if d > NOISE_FILTER:
#            print( "data old = " + str(self.data_old[PUENTE_ON[i]]))
#            print( "data = " + str(self.data[PUENTE_ON[i]]))

            if( self.data[PUENTE_ON[i]] != self.data_old[PUENTE_ON[i]]):
                self.MIDI.note_on( PUENTE_NOTES[i], 127, channel = 2 )
                logging.debug("PUENTE_ON: " + str(i) )
            elif( self.data[PUENTE_OFF[i]] != self.data_old[PUENTE_OFF[i]]):
                self.MIDI.note_off( PUENTE_NOTES[i], 127, channel = 2 )
                logging.debug("PUENTE_OFF: " + str(i) )

    def handle_timon(self):
        if (int(self.data[BPM]) != int(self.data_old[BPM])):
            x = self.normalize(int(self.data[BPM]),
                               old_min=20, old_max=999, new_min = 10, new_max = 32)
            self.MIDI.control_change(BPM_CC, int(x))
#        self.MIDI.

    def handle_seres(self):
    # Selector
        channel = [6, 7, 8, 9, 10, 11]
        j = 0
        for i in range( 6 ) :
            if( self.data[SERES_ISLA[i]] == "1" ) :
                j = i

            if (self.data[SERES_ISLA[i]] != self.data_old[SERES_ISLA[i]]):
                logging.debug("ARP["+ str(i) + "] = " + str(self.arp_state[j]))
                self.MIDI.note_on(STOP_NOTE, 127, 1)
                if(self.arp_state[j] == 1 ) :
#                    self.MIDI.note_on(self.ARP_NOTE[j], 127, 1)
                    self.arp_state[j] = 0
    # Arpeggiator
#        logging.debug("ARP: " + self.data[ARPEGIATOR])
        if ( int(self.data[ARPEGIATOR]) != int(self.data_old[ARPEGIATOR]) ):
            if(int(self.data[ARPEGIATOR]) == 0) :
                logging.debug("ARP")
                self.MIDI.note_on( ARP_NOTE[j], 127, 1 )
                self.arp_state[j] = not self.arp_state[j]

    # Slide Ribbons
        min_note = 60
        max_note = 116 #96
        no_note_value = 44 #78 44
        note = int(self.normalize( int(self.data[SLIDE_RIBBON[1]]),
                                old_min = 0, old_max = 127, new_min = min_note, new_max = max_note ))
        if (self.data_old[SLIDE_RIBBON[1]] != self.data[SLIDE_RIBBON[1]]):
            print( "data old = " + str(self.data_old[SLIDE_RIBBON[1]]))
            print( "data = " + str(self.data[SLIDE_RIBBON[1]]))
            if True:
#            if(int(self.data_old[SLIDE_RIBBON[1]]) == no_note_value)  :
#                (int(self.data[SLIDE_RIBBON[1]]) != no_note_value) ) :
                self.MIDI.note_on(int(note), 127, channel[j])
                logging.debug("SERES NOTE_ON: " + str(note))
                self.MIDI.note_off(self.seres_last_note, 0, channel[j])
                logging.debug("SERES NOTE_OFF: " + str(note))
                self.seres_last_note = note
                self.MIDI.control_change(RIBBON_CC, int(self.data[SLIDE_RIBBON[1]]), channel = 1)
                logging.debug("SERES CC: " + str(self.data[SLIDE_RIBBON[1]]))
            if( int(self.data[SLIDE_RIBBON[1]]) == no_note_value ) :
                self.MIDI.note_off(self.seres_last_note, 0, channel[j])
                logging.debug("SERES NOTE_OFF: " + str(note))
    # MIC
        if (self.data[MIC_BUTTON] != self.data_old[MIC_BUTTON]):
            if (int(self.data[MIC_BUTTON]) == 0):
                self.MIDI.note_on(MIC_REC_NOTE, 127, channel = 1)
                logging.debug("MIC NOTE_ON: " + str(MIC_REC_NOTE))

            else:
                self.MIDI.note_on(MIC_PLAY_NOTE, 127, channel = 1)
                logging.debug("MIC NOTE_ON: " + str(MIC_PLAY_NOTE))

    def handle_cueva(self):
        for n in range(6):
            m = n - 1
            if (n == 0): m = 5
            if ((self.data[INDEX] == str(n)) & # INDEX, the number of the SW on
                    (self.data[SW[n]] == "1")):
                if(self.data[CUEVA_SEL[0]] == "1"):
                    self.MIDI.note_on(SEQ_1_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_1_NOTE[n], 127, 5)
                    self.MIDI.note_on(PLAY_NOTE,127,1)

                if(self.data[CUEVA_SEL[1]]== "1"):
                    self.MIDI.note_on(SEQ_2_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_2_NOTE[n], 127, 5)
                    self.MIDI.note_on(PLAY_NOTE,127,1)
                if(self.data[CUEVA_SEL[2]]== "1"):
                    self.MIDI.note_on(SEQ_3_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_3_NOTE[n], 127, 5)
                    self.MIDI.note_on(PLAY_NOTE,127,1)

                logging.debug( "CUEVA_SEL 0 = " + str(self.data[CUEVA_SEL[0]]) )
                logging.debug( "CUEVA_SEL 1 = " + str(self.data[CUEVA_SEL[1]]) )
                logging.debug( "CUEVA_SEL 2 = " + str(self.data[CUEVA_SEL[2]]) )

#            if (self.data[CUEVA_SEL[0]] == "1"): 
                # Encoders (antiguos pots)

            THRES = 1
            if( self.data[POT[0]] !=
                self.data_old[POT[0]]) :
                    self.MIDI.control_change( POT_CC[0],
                                         int( self.data[POT[0]]) )
            if( self.data[POT[1]] !=
                self.data_old[POT[1]] ) :
                    self.MIDI.control_change( POT_CC[1],
                                int( self.data[POT[1]]) )
    def handle_ambientes(self):
#        logging.debug( "AMBIENTE: " + self.data[SELVA_SEL[0]] + ", " +
#                      self.data[SELVA_SEL[1]] + ", " +
#                      self.data[SELVA_SEL[2]] + ", " +
#                      self.data[SELVA_SEL[3]] )
        note_offset = 0 
        for i in range( 4 ) :
#            if( (int(self.data[SELVA_SEL[i]]) !=
#                    int(self.data_old[SELVA_SEL[i]])) &
#                    (int(self.data[SELVA_SEL[i]]) > 0) ):
#                self.MIDI.note_on( SELVA_SEL_NOTES[i], 127, channel = 1 )
#                logging.debug("AMBIENTE " + str(i) + "  NOTE: " + str(SELVA_SEL_NOTES[i]) )
#                time.sleep(0.9)
            if( int(self.data[SELVA_SEL[i]]) == 1 ):
                note_offset = i*16

        # Pulsadores one_shot tipo arcade
        for i in range(6):
            if ((self.data[SELVA_ONE_SHOT[i]] == "1") &
                    (self.data_old[SELVA_ONE_SHOT[i]] == "0")):
                self.MIDI.note_on(SELVA_ONE_SHOT_NOTES[i] + note_offset, 127, channel = 4)
                logging.debug( "ONE_SHOT_NOTE_ON " + str(i) )
            if ((self.data[SELVA_ONE_SHOT[i]] == "0") &
                    (self.data_old[SELVA_ONE_SHOT[i]] == "1")):
                self.MIDI.note_off(SELVA_ONE_SHOT_NOTES[i] + note_offset, 127, channel = 4)
                logging.debug( "ONE_SHOT_NOTE_OFF " + str(i) )
                self.ambiente_last_note = SELVA_ONE_SHOT_NOTES[i]
        # joystick
        X_MIN = 390
        X_N = 470
        X_MAX = 610
        X_THRES = 3

        Y_MIN = 390
        Y_N = 470
        Y_MAX = 610
        Y_THRES = 3

#        logging.debug("joy x: " + self.data[JOY_X] +
#                      "joy y: " + self.data[JOY_Y])

        if ( abs(int(self.data[JOY_X]) -
              int(self.data_old[JOY_X])) > X_THRES):
            x = self.normalize(int(self.data[JOY_X]),
                               X_MIN, X_MAX, 0, 127)
        #    self.MIDI.control_change( self.JOY[0], int(x))
        #    self.MIDI.control_change( self.JOY[1], int(x))

        if ( abs(int(self.data[JOY_Y]) -
              int(self.data_old[JOY_Y])) > Y_THRES):
            x = self.normalize(int(self.data[JOY_Y]),
                               Y_MIN, Y_MAX, 0, 127)
         #   self.MIDI.control_change( self.JOY[0], int(x))
         #   self.MIDI.control_change( self.JOY[2], int(x))

    def run(self):
        i = 0
        try:
            while(True) :
# update data
                self.data = self.q.get()
                if(i == 0 ) :
                    self.data_old = self.data
                    i+=1
                self.handle_lorito()
                self.handle_puente()
                self.handle_tunel()
                self.handle_timon()
                self.handle_ambientes()
                self.handle_seres()
                self.handle_cueva()
                self.data_old = self.data
        except KeyboardInterrupt:
            self.close()

    def normalize( self, x_in, old_min = 0, old_max = 1023, new_min = 0, new_max = 127 ) :
        x_out = ( (x_in - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
        if(x_out < new_min) : x_out = new_min
        if(x_out > new_max) : x_out = new_max
        return (x_out)
