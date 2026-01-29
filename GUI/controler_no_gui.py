
from MIDI_interface import *
from serial_interface import *

import wx
import threading
import time
import random
import logging
import queue
import elements

class Controler(threading.Thread, serial_interface):
    """Main Control: read data and generate MIDI messages"""
    N_DATA = 46 # number of received parameteres
    N_Q = 3 # number of data queues. Each queue goes to each thread.
    
    def __init__( self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        self.MIDI = MIDI_interface()
        midi_port = self.MIDI.connect()

        self.MIDI.test_note_on()

        self.open_port()
        self.q = []
        for n in range (self.N_Q):
            self.q.append(queue.Queue())

        self.loroloco = elements.LoroLoco(2, "loroloco_thread", self.q[0], self.MIDI)
        self.sequencer = elements.Secuenciador(3, "sequencer_thread", self.q[1], self.MIDI)
        self.states_diagram = elements.StatesDiagram(4, "states_diagram_thread", self.q[2], self.MIDI)

    def run(self):

        self.loroloco.start()
        self.sequencer.start()

        i = 0
        while( True ):
            # lectura datos puerto serie
            self.data = self.read_serial_data().split(',')

            # test datos puerto serie

            if( len( self.data ) != self.N_DATA ) : 
                print("WARNING reading serial data")
                print("n_data = ")
                print(len(self.data))
                print(self.data)
                self.data = ""
            else:
#                print(len(self.data))
#                print(self.data)
                for n in range (self.N_Q):
                    self.q[n].put(self.data)

# LORO
# PUENTE
# TUNEL 
# TIMON
# SERES ISLA
# CUEVA RUIDOS
# SELVA_AMBIENTE

################################################
