# Serial data IDs. Coordinado con Arduino
#    PUENTE = [0,1,2,3,4,5]
SONAR = 0 # TODO: este va a ir con ESP32 tambien
TIMON = 1
ARPEGIATOR = 2
MIC_BUTTON = 3
SERES_ISLA = [4, 5, 6, 7, 8, 9]
SLIDE_RIBBON = [10, 11]
CUEVA_SEL = [12, 13, 14]
SW = [15, 16, 17, 18, 19, 20]
POT = [21, 22]
SELVA_ONE_SHOT = [23, 24, 25, 26, 27, 28]
SELVA_SEL = [29, 30, 31, 32]
JOY_X = 33
JOY_Y = 34
BPM = 35
TEMPO = 36 
INDEX = 37
DATA = 38 # Serial.availableForWrite
N = 39      # num of serial data items

# OSC data IDs. Coordinado con Arduino
PUENTE = [40, 41, 42, 43, 44, 45] #plataformas del puente: force
LORITO = [46, 47, 48, 49] # lorito de peluche: movement, pith, roll, pressure

# MIDI msg data
ARP_NOTE = [60, 61, 62, 63, 64, 65]
RIBBON_CC = 26
RIBBON_NOTE = 60
SEQ_1_NOTE = [36, 37, 38, 39, 40, 41]
SEQ_2_NOTE = [44, 45, 46, 47, 48, 49]
SEQ_3_NOTE = [52, 53, 54, 55, 56, 57]
POT_CC = [20,21]
SELVA_ONE_SHOT_NOTES = [36, 37, 38, 40, 41, 42]     # C2, D2, E2, F2, G2, A2
SELVA_SEL_NOTES = [72, 73, 74, 75]
JOY_CC = [12, 22, 23]
BPM_CC = 19
TUNEL_NOTE = 84
TUNEL_CC = 24
PUENTE_NOTES = [41, 40, 39, 38, 37, 36]
STOP_NOTE = 38
LORITO_NOTE = 84 #TODO
