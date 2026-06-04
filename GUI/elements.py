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

    def handle_lorito(self):
        LORITO_ON_THRES = 10
        LORITO_OFF_THRES = 20
        if(self.data[LORITO[0]] > LORITO_ON_THRES ):
            self.MIDI.note_on(LORITO_NOTE, self.data[LORITO[0]] )

    def handle_tunel(self):
        SONAR_THRES = 80   #cm
        NOISE_THRES = 12

        if( int(self.data[SONAR]) > NOISE_THRES ) :
            self.d = int(self.data[SONAR] )
            logging.debug("SONAR: " + self.data[SONAR] )

        if( (self.d < SONAR_THRES ) &
            (self.d_old > SONAR_THRES)):
            self.MIDI.note_on( self.TUNEL_NOTE, 127, channel = 1 )

        self.d_old = self.d

    def handle_puente(self):
        PUENTE_ON_THRES = [160, 160, 160, 160, 160, 160]
        PUENTE_OFF_THRES = [100, 100, 100, 100, 100, 100]

#        logging.debug("  data = "
#              + str( self.data[PUENTE[0]] + ", ")
#              + str( self.data[PUENTE[1]] + ", ")
#              + str( self.data[PUENTE[2]] + ", ")
#              + str( self.data[PUENTE[3]] + ", ")
#              + str( self.data[PUENTE[4]] + ", ")
#              + str(self.data[PUENTE[5]]))

        for i in range(6):
            d = int(self.data[PUENTE[i]]) - int(self.data_old[PUENTE[i]])
        #                d = abs(d)

            if((int(self.data[PUENTE[i]]) > PUENTE_ON_THRES[i]) &
                    (int(self.data_old[PUENTE[i]]) < PUENTE_ON_THRES[i])) :
                self.MIDI.note_on( PUENTE_NOTES[i], 127, channel = 2 )
#                print(str(i) + "  NOTE_ON " + str(self.PUENTE_NOTES[i]) +
#                  "   data = " + self.data[PUENTE[i]] +
#                  "   data_old = " + self.data_old[PUENTE[i]] + "  d = " + str(d))
#            if( False ):
#            if (d < -self.PUENTE_OFF_THRES[i]):
            if ((int(self.data[PUENTE[i]]) < PUENTE_ON_THRES[i]) &
                    (int(self.data_old[PUENTE[i]]) > PUENTE_ON_THRES[i])):
                #                    d = self.normalize(d, old_min = 0, old_max = 1023)
                self.MIDI.note_off( PUENTE_NOTES[i], 127, channel = 2 )
#                print(str(i) + "  NOTE_OFF " + str(self.PUENTE_NOTES[i]) +
#                "   data = " + self.data[PUENTE[i]] +
#                "   data_old = " + self.data_old[osc_interface.PUENTE[i]] + "  d = " + str(d))

    def handle_timon(self):
        if (int(self.data[BPM]) != int(self.data_old[BPM])):
            x = self.normalize(int(self.data[BPM]),
                               old_min=20, old_max=999, new_min = 10, new_max = 32)
            self.MIDI.control_change(BPM_CC, int(x))

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
            if(int(self.data[ARPEGIATOR]) == 1) :
                logging.debug("ARP")
                self.MIDI.note_on( ARP_NOTE[j], 127, 1 )
                self.arp_state[j] = not self.arp_state[j]
    # Slide Ribbons
        min_note = 17
        max_note = 90
        note_old = 17
#        note = self.normalize( int(self.data[SLIDE_RIBBON[0]]),
#                                old_min = 0, old_max = 1023, new_min = min_note, new_max = max_note )
        thres = 100   # to filter noise when ribbon is not pushed
        if((int(self.data[SLIDE_RIBBON[0]]) > thres)):
            if(int(self.data_old[SLIDE_RIBBON[0]]) < thres ):
                self.MIDI.note_on(RIBBON_NOTE, 127, channel[j])
                logging.debug("SERES NOTE_ON: " + str(self.data[SLIDE_RIBBON[0]]))
            if( int(self.data[SLIDE_RIBBON[0]]) !=
                int(self.data_old[SLIDE_RIBBON[0]]) ):
                control = self.normalize( int(self.data[SLIDE_RIBBON[0]]),
                    old_min = 1023, old_max = 940, new_min = 0, new_max = 127 )
                self.MIDI.control_change( RIBBON_CC, int(control), channel = 1 )
        if ((int(self.data_old[SLIDE_RIBBON[0]]) > thres ) &
                (int(self.data[SLIDE_RIBBON[0]]) < thres) ):
            self.MIDI.note_off( RIBBON_NOTE, 127, channel[j])
            logging.debug("SERES NOTE_OFF: " +
                          str(self.data[SLIDE_RIBBON[1]])+ ", " +
                          str(self.data_old[SLIDE_RIBBON[1]]))

        if((int(self.data[SLIDE_RIBBON[1]]) > thres)):
            if(int(self.data_old[SLIDE_RIBBON[1]]) < thres ):
                k = j
                if(j == 5): k = 0
                self.MIDI.note_on(RIBBON_NOTE, 127, channel[k])
                logging.debug("SERES NOTE_ON: " + str(self.data[SLIDE_RIBBON[0]]))
            if( int(self.data[SLIDE_RIBBON[1]]) !=
                int(self.data_old[SLIDE_RIBBON[1]]) ):
                control = self.normalize( int(self.data[SLIDE_RIBBON[0]]),
                    old_min = 1023, old_max = 940, new_min = 0, new_max = 127 )
                self.MIDI.control_change( RIBBON_CC, int(control), channel = 1 )
        if ((int(self.data_old[SLIDE_RIBBON[1]]) > thres ) &
                (int(self.data[SLIDE_RIBBON[1]]) < thres) ):
            k = j
            if (j == 5): j = 0
            self.MIDI.note_off( RIBBON_NOTE, 127, channel[k])
            logging.debug("SERES NOTE_OFF: " +
                          str(self.data[SLIDE_RIBBON[1]])+ ", " +
                          str(self.data_old[SLIDE_RIBBON[1]]))

    def handle_cueva(self):
        for n in range(6):
            m = n - 1
            if (n == 0): m = 5
            if ((self.data[INDEX] == str(n)) & # INDEX, the number of the SW on
                    (self.data[SW[n]] == "1")):
                if(self.data[CUEVA_SEL[0]] == "1"):
                    self.MIDI.note_on(SEQ_1_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_1_NOTE[n], 127, 5)
                if(self.data[CUEVA_SEL[1]]== "1"):
                    self.MIDI.note_on(SEQ_2_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_2_NOTE[n], 127, 5)
                if(self.data[CUEVA_SEL[2]]== "1"):
                    self.MIDI.note_on(SEQ_3_NOTE[n], 127, 5)
                    self.MIDI.note_off(SEQ_3_NOTE[n], 127, 5)

#                logging.debug( "CUEVA_SEL 0 = " + str(self.data[CUEVA_SEL[0]]) )
#                logging.debug( "CUEVA_SEL 1 = " + str(self.data[CUEVA_SEL[1]]) )
#                logging.debug( "CUEVA_SEL 2 = " + str(self.data[CUEVA_SEL[2]]) )

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
        for i in range( 4 ) :
            if( (int(self.data[SELVA_SEL[i]]) !=
                    int(self.data_old[SELVA_SEL[i]])) &
                    (int(self.data[SELVA_SEL[i]]) > 0) ):
                self.MIDI.note_on( SELVA_SEL_NOTES[i], 127, channel = 1 )

                logging.debug("AMBIENTE " + str(i) + "  NOTE: " + str(self.SELVA_SEL_NOTES[i]) )
#                time.sleep(0.9)
        # Pulsadores one_shot tipo arcade
        for i in range(6):
            if ((self.data[SELVA_ONE_SHOT[i]] == "1") &
                    (self.data_old[SELVA_ONE_SHOT[i]] == "0")):
                self.MIDI.note_on(SELVA_ONE_SHOT[i], 127, channel = 4)
                logging.debug( "ONE_SHOT " + str(i) )
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
