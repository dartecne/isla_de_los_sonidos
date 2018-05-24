
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
    N_DATA = 43 # number of received parameteres
    
    def __init__( self, threadID, name, gui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.gui = gui
        
        self.loroloco = elements.LoroLoco(2, "loroloco_thread")

        self.MIDI = MIDI_interface()
        self.MIDI.connect()
        self.MIDI.test_note_on()

        self.open_port()

        self.q = queue.Queue()
        self.loroloco.set_queue( self.q )
        self.loroloco.set_MIDI( self.MIDI )

    def get_queue(self):
        return self.q

    def run(self):

        self.loroloco.start()

        i = 0
        while( True ):
            # lectura datos puerto serie
            self.data = self.read_serial_data().split(',')

            if( i == 0 ) :  # first iteration 
                self.data_old = self.data
                i+=1

            # test datos puerto serie

            if( len( self.data ) != self.N_DATA ) : 
                print("WARNING reading serial data")
                print("n_data = ")
                print(len(self.data))
                print(self.data)
                print(len(self.data))
                print(self.data)
                self.data = ""
            else:
            # test datos puerto serie
                self.q.put(self.data)
                self.update_gui_values()
                self.data_old = self.data

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

# LORO
        self.gui.m_checkBox_loro_rec.SetValue(bool(int(self.data[serial_interface.LORO_REC])))

# TIMON
        self.gui.m_textCtrl_timon.SetValue(self.data[8])

# SERES ISLA
        self.gui.m_checkBox_arpegiator.SetValue(bool(int(self.data[9])))

        self.gui.m_radioBtn_ser1.SetValue(bool(int(self.data[10])))
        self.gui.m_radioBtn_ser2.SetValue(bool(int(self.data[11])))
        self.gui.m_radioBtn_ser3.SetValue(bool(int(self.data[12])))
        self.gui.m_radioBtn_ser4.SetValue(bool(int(self.data[13])))
        self.gui.m_radioBtn_ser5.SetValue(bool(int(self.data[14])))
        self.gui.m_radioBtn_ser6.SetValue(bool(int(self.data[15])))

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
        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[1]])))
        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[2]])))
        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[3]])))
        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[4]])))
        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[serial_interface.SELVA_ONE_SHOT[5]])))

        self.gui.m_textCtrl_joy_x.SetValue(self.data[serial_interface.JOY_X])
        self.gui.m_textCtrl_joy_y.SetValue(self.data[serial_interface.JOY_Y])

