
import csv
from datetime import datetime
import wx
import threading
import time
import random
import logging
import queue

import elements
from MIDI_interface import *
from serial_interface import *
from osc_interface import *
from elements_ids import *
from GUI import *

class Controler(threading.Thread, serial_interface, osc_interface):
    """Main Control: read data and generate MIDI messages"""
    N_SERIAL_DATA = 40 # number of received parameteres by serial port
    N_Q = 3 # number of data queues. Each queue goes to each thread.
    HEAD = ["SONAR", "TIMON", "ARPEGIATOR", "MIC_BUTTON", "SERES_ISLA",
    "SLIDE_RIBBON", "CUEVA_SEL", "SW", "POT", "SELVA_ONE_SHOT", "SELVA_SEL",
    "JOY_X", "JOY_Y", "BPM", "TEMPO", "PUENTE", "LORITO"]

    def __init__( self, threadID, name, gui_flag):
        self.open_log()
        self.gui_flag = gui_flag
        logging.info(f"Controller with gui: {self.gui_flag}")
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        osc_interface.__init__(self)

        self.MIDI = MIDI_interface()
        midi_port = self.MIDI.connect()

        self.MIDI.test_note_on()

        self.sp = self.open_serial_port()
        self.q = []
        for n in range (self.N_Q):
            self.q.append(queue.Queue())

        self.sequencer = elements.Secuenciador(3, "sequencer_thread", self.q[1], self.MIDI)
        self.states_diagram = elements.StatesDiagram(4, "states_diagram_thread", self.q[2], self.MIDI)

    def set_GUI(self, gui):
        self.gui = gui

    def run(self):
        try:
            self.sequencer.start() # handel all LISA elements: OSC and Serial

            i = 0
            while( True ):
                # lectura datos puerto serie
                if self.sp != None:
                    self.serial_data = self.read_serial_data().split(',')

                # test datos puerto serie
                    if( len( self.serial_data ) != self.N_SERIAL_DATA ) : 
                        print("WARNING reading serial data.")
                        print("n_data = ")
                        print(len(self.serial_data))
                        print(self.serial_data)
                        # Han fallado los datos, ponemos todo a 0
                        self.serial_data = [0] * self.N_SERIAL_DATA
        #           else:
        #                print(len(self.data))
        #                print(self.data)
                else: # No hay puerto serial, ponemos todo a 0
                    self.serial_data = [0] * self.N_SERIAL_DATA

                # lectura datos OSC
                self.data_osc = self.parse_osc_data()
                if self.data_osc == None:
#                    print("WARNING reading OSC data gave None")
                    self.data_osc = [0] * self.N_OSC_DATA

                self.data = self.serial_data + self.data_osc
                self.log_data(self.data)
                for n in range (self.N_Q):
                    self.q[n].put(self.data)
                if self.gui_flag:
                    self.update_gui_values()

        except KeyboardInterrupt:
            self.close()

    def open_log(self):
        filename = datetime.now().strftime("lisa_data_%Y%m%d_%H%M%S.csv")
        self.log_file = open(filename, "w", newline="")
        self.log_writer = csv.writer(self.log_file)

        self.log_writer.writerow(
            ["timestamp"] +
            [addr.replace("/", "_") for addr in self.HEAD]
        )

        self.log_counter = 0
        logging.info(f"Log de datos guardado en: {filename}")

    def log_data(self, data_array):
        timestamp = datetime.now().timestamp()
        self.log_writer.writerow([timestamp] + data_array)
        self.log_counter += 1
    
        # Flush cada 100 muestras
        if self.log_counter >= 100:
            self.log_file.flush()
            self.log_counter = 0

    def close(self):
        osc_interface.close(self)
        self.raise_exception()

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# LORO
# PUENTE
# TUNEL 
# TIMON
# SERES ISLA
# CUEVA RUIDOS
# SELVA_AMBIENTE

    def update_gui_values(self):
        self.gui.m_textCtrl_inputs.SetValue( str(self.data) )

# PUENTE
#        self.gui.m_textCtrl_puente_1.SetValue(str(self.data[0]))
#        self.gui.m_textCtrl_puente_2.SetValue(self.data[1])
#        self.gui.m_textCtrl_puente_3.SetValue(self.data[2])
#        self.gui.m_textCtrl_puente_4.SetValue(self.data[3])
#        self.gui.m_textCtrl_puente_5.SetValue(self.data[4])
#        self.gui.m_textCtrl_puente_6.SetValue(self.data[5])
# TUNEL
        self.gui.m_textCtrl_tunel_sonar.SetValue(self.data[SONAR])
#        self.gui.m_textCtrl_tunel_sonar.SetValue(self.data[BPM])

# LORO
#        self.gui.m_checkBox_loro_rec.SetValue(bool(int(self.data[LORO_REC])))

# TIMON
        #self.gui.m_textCtrl_timon.SetValue(self.data[BPM])
        self.gui.m_textCtrl_timon.SetValue(self.data[TIMON])

# SERES ISLA
        self.gui.m_checkBox_arpegiator.SetValue(bool(int(self.data[ARPEGIATOR])))

        self.gui.m_radioBtn_ser1.SetValue(bool(int(self.data[SERES_ISLA[0]])))
        self.gui.m_radioBtn_ser2.SetValue(bool(int(self.data[SERES_ISLA[1]])))
        self.gui.m_radioBtn_ser3.SetValue(bool(int(self.data[SERES_ISLA[2]])))
        self.gui.m_radioBtn_ser4.SetValue(bool(int(self.data[SERES_ISLA[3]])))
        self.gui.m_radioBtn_ser5.SetValue(bool(int(self.data[SERES_ISLA[4]])))
        self.gui.m_radioBtn_ser6.SetValue(bool(int(self.data[SERES_ISLA[5]])))

        self.gui.m_textCtrl_slide_1.SetValue(self.data[SLIDE_RIBBON[0]])
        self.gui.m_textCtrl_slide_2.SetValue(self.data[SLIDE_RIBBON[1]])

# CUEVA RUIDOS
        self.gui.m_radioBtn_cueva_1.SetValue(bool(int(self.data[CUEVA_SEL[0]])))
        self.gui.m_radioBtn_cueva_2.SetValue(bool(int(self.data[CUEVA_SEL[1]])))
        self.gui.m_radioBtn_cueva_3.SetValue(bool(int(self.data[CUEVA_SEL[2]])))

        self.gui.m_checkBox_seq_1.SetValue(bool(int(self.data[SW[0]])))
        self.gui.m_checkBox_seq_2.SetValue(bool(int(self.data[SW[1]])))
        self.gui.m_checkBox_seq_3.SetValue(bool(int(self.data[SW[2]])))
        self.gui.m_checkBox_seq_4.SetValue(bool(int(self.data[SW[3]])))
        self.gui.m_checkBox_seq_5.SetValue(bool(int(self.data[SW[4]])))
        self.gui.m_checkBox_seq_6.SetValue(bool(int(self.data[SW[5]])))

        self.gui.m_textCtrl_pot_1.SetValue(self.data[POT[0]])
        self.gui.m_textCtrl_pot_2.SetValue(self.data[POT[1]])

# SELVA_AMBIENTE
        self.gui.m_radioBtn_ambiente_1.SetValue(bool(int(self.data[SELVA_SEL[0]])))
        self.gui.m_radioBtn_ambiente_2.SetValue(bool(int(self.data[SELVA_SEL[1]])))
        self.gui.m_radioBtn_ambiente_3.SetValue(bool(int(self.data[SELVA_SEL[2]])))
        self.gui.m_radioBtn_ambiente_4.SetValue(bool(int(self.data[SELVA_SEL[3]])))

        self.gui.m_checkBox_one_shot_1.SetValue(bool(int(self.data[SELVA_ONE_SHOT[0]])))
        self.gui.m_checkBox_one_shot_2.SetValue(bool(int(self.data[SELVA_ONE_SHOT[1]])))
        self.gui.m_checkBox_one_shot_3.SetValue(bool(int(self.data[SELVA_ONE_SHOT[2]])))
        self.gui.m_checkBox_one_shot_4.SetValue(bool(int(self.data[SELVA_ONE_SHOT[3]])))
        self.gui.m_checkBox_one_shot_5.SetValue(bool(int(self.data[SELVA_ONE_SHOT[4]])))
        self.gui.m_checkBox_one_shot_6.SetValue(bool(int(self.data[SELVA_ONE_SHOT[5]])))

        self.gui.m_textCtrl_joy_x.SetValue(self.data[JOY_X])
        self.gui.m_textCtrl_joy_y.SetValue(self.data[JOY_Y])


