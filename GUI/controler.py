
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
    
    def __init__( self, threadID, name, gui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.gui = gui
        
        self.MIDI = MIDI_interface()
        midi_port = self.MIDI.connect()
        self.gui.m_textCtrl_outputs.SetValue( "Connected to MIDI port: " + str(midi_port) )

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
#        self.states_diagram.start()

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
                self.update_gui_values()

# LORO
# PUENTE
# TUNEL 
# TIMON
# SERES ISLA
# CUEVA RUIDOS
# SELVA_AMBIENTE

################################################
    def update_gui_values(self):
        self.gui.m_textCtrl_inputs.SetValue( str(self.data) )

# PUENTE
        self.gui.m_textCtrl_puente_1.SetValue(str(self.data[0]))
        self.gui.m_textCtrl_puente_2.SetValue(self.data[1])
        self.gui.m_textCtrl_puente_3.SetValue(self.data[2])
        self.gui.m_textCtrl_puente_4.SetValue(self.data[3])
        self.gui.m_textCtrl_puente_5.SetValue(self.data[4])
        self.gui.m_textCtrl_puente_6.SetValue(self.data[5])
# TUNEL
        self.gui.m_textCtrl_tunel_sonar.SetValue(self.data[6])
#        self.gui.m_textCtrl_tunel_sonar.SetValue(self.data[serial_interface.BPM])

# LORO
        self.gui.m_checkBox_loro_rec.SetValue(bool(int(self.data[serial_interface.LORO_REC])))

# TIMON
        self.gui.m_textCtrl_timon.SetValue(self.data[serial_interface.BPM])

# SERES ISLA
        self.gui.m_checkBox_arpegiator.SetValue(bool(int(self.data[9])))

        self.gui.m_radioBtn_ser1.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[0]])))
        self.gui.m_radioBtn_ser2.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[1]])))
        self.gui.m_radioBtn_ser3.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[2]])))
        self.gui.m_radioBtn_ser4.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[3]])))
        self.gui.m_radioBtn_ser5.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[4]])))
        self.gui.m_radioBtn_ser6.SetValue(bool(int(self.data[serial_interface.SERES_ISLA[5]])))

        self.gui.m_textCtrl_slide_1.SetValue(self.data[16])
        self.gui.m_textCtrl_slide_2.SetValue(self.data[17])

# CUEVA RUIDOS
        self.gui.m_radioBtn_cueva_1.SetValue(bool(int(self.data[18])))
        self.gui.m_radioBtn_cueva_2.SetValue(bool(int(self.data[19])))
        self.gui.m_radioBtn_cueva_3.SetValue(bool(int(self.data[20])))

        self.gui.m_checkBox_seq_1.SetValue(bool(int(self.data[21])))
        self.gui.m_checkBox_seq_2.SetValue(bool(int(self.data[22])))
        self.gui.m_checkBox_seq_3.SetValue(bool(int(self.data[23])))
        self.gui.m_checkBox_seq_4.SetValue(bool(int(self.data[24])))
        self.gui.m_checkBox_seq_5.SetValue(bool(int(self.data[25])))
        self.gui.m_checkBox_seq_6.SetValue(bool(int(self.data[26])))

        self.gui.m_textCtrl_pot_1.SetValue(self.data[27])
        self.gui.m_textCtrl_pot_2.SetValue(self.data[28])

# SELVA_AMBIENTE
        self.gui.m_radioBtn_ambiente_1.SetValue(bool(int(self.data[serial_interface.SELVA_SEL[0]])))
        self.gui.m_radioBtn_ambiente_2.SetValue(bool(int(self.data[serial_interface.SELVA_SEL[1]])))
        self.gui.m_radioBtn_ambiente_3.SetValue(bool(int(self.data[serial_interface.SELVA_SEL[2]])))
        self.gui.m_radioBtn_ambiente_4.SetValue(bool(int(self.data[serial_interface.SELVA_SEL[3]])))

        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[0]])))
        self.gui.m_checkBox_one_shot_2.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[1]])))
        self.gui.m_checkBox_one_shot_3.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[2]])))
        self.gui.m_checkBox_one_shot_4.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[3]])))
        self.gui.m_checkBox_one_shot_5.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[4]])))
        self.gui.m_checkBox_one_shot_6.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[5]])))

        self.gui.m_textCtrl_joy_x.SetValue(self.data[serial_interface.JOY_X])
        self.gui.m_textCtrl_joy_y.SetValue(self.data[serial_interface.JOY_Y])

