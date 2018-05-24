import threading
import logging
import time
import random

from serial_interface import *

class Element( threading.Thread ):

    def __init__( self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def set_queue( self, q ):
        self.q = q

    def set_MIDI( self, MIDI ):
        self.MIDI = MIDI

class LoroLoco( Element ):
    LORO_REC = "C-4"
    LORO_PLAY = "D-4"
    LORO_STOP = "E-4"

    def run(self):
        i = 0
        while( True):
         self.data = self.q.get()
         if(i == 0 ) :
             self.data_old = self.data
             i+=1
         r = random.randint(0,24)
         if(r == 1) : self.MIDI.note_on( self.LORO_STOP, 127 )

         if( (self.data[serial_interface.LORO_REC] == "1") &
           (self.data_old[serial_interface.LORO_REC] == "0") ) :
            self.MIDI.note_on( self.LORO_REC, 127 )
            logging.debug( "LORO REC!!!" )
         elif((self.data[serial_interface.LORO_REC] == "0") &
           (self.data_old[serial_interface.LORO_REC] == "1") ) :
            self.MIDI.note_on( self.LORO_PLAY, 127 )
            logging.debug( "LORO PLAY!!!" )
            time.sleep(4)
            self.MIDI.note_on( self.LORO_STOP, 127 )
            logging.debug( "LORO STOP!!!" )
         self.data_old = self.data

