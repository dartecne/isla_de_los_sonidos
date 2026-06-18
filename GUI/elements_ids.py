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
PUENTE_FORCE = [40, 43, 46, 49, 52, 55] #plataformas del puente: force
PUENTE_ON = [41, 44, 47, 50, 53, 56] #plataformas del puente: force
PUENTE_OFF = [42, 45, 48, 51, 54, 57] #plataformas del puente: force

LORITO = [58, 59, 60, 61] # lorito de peluche: movement, pith, roll, pressure


# MIDI msg data
# channel 1 - controlers
STOP_NOTE = 38
MIC_REC_NOTE = 48
MIC_PLAY_NOTE = 50
MIC_STOP_NOTE = 52
ARP_NOTE = [60, 61, 62, 64, 65, 66] # C3, C#3, D3, D#3, E3, F3
RIBBON_NOTE = 60 # no se para que se usa
LORITO_NOTE = 24 
PLAY_NOTE = 26
SEQ_1_NOTE = [36, 37, 38, 39, 40, 41]
SEQ_2_NOTE = [44, 45, 46, 47, 48, 49]
SEQ_3_NOTE = [52, 53, 54, 55, 56, 57]
SELVA_ONE_SHOT_NOTES = [36, 37, 38, 39, 40, 41]     # C1, D1, E1, F1, G1, A1
SELVA_SEL_NOTES = [72, 73, 74, 75] # C4, C#4, D4, D#4
TUNEL_NOTE = 84
RIBBON_CC = 26
PUENTE_NOTES = [41, 40, 39, 38, 37, 36]

JOY_CC = [12, 22, 23]
BPM_CC = 19
POT_CC = [20, 21]
TUNEL_CC = 22
LORITO_CC = [24, 25]

