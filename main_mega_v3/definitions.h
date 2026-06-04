#pragma once

#define NUM_LEDS 6
#define NUM_CUEVA_SEL	3
#define NUM_SELVA_ONE_SHOT	6
#define NUM_SELVA_SEL	4
#define NUM_SW	6
#define NUM_SERES_SEL	6
#define NUM_PUENTE_PIEZOS	6

//TIMON
#define PS2DATA   22
#define PS2CLOCK  24

//#define BAUDRATE	57600
//#define BAUDRATE	9600
#define BAUDRATE	115200

int tunel_echo = 6;  
int tunel_trigger= 7;	
long sonar_value = 0;


//TIMON
long timon_data_value = 0;

// CUEVA DE LOS RUIDOS
int cueva_sel_pin[] = { 32, 30, 28 };
int cueva_sel_value[] = { 0, 0, 0 };
int sw_pin[] = { 23, 25, 27, 31, 29, 33 }; 
int sw_value[] = { 0, 0, 0, 0, 0, 0 };
//int led_pin[] = { 8, 9, 10, 11, 12, 13};
int led_pin[] = { 13, 12, 11, 10, 9, 8};
int led_value[] = { 0, 0, 0, 0, 0 };

// SELVA SONIDOS AMBIENTE

int selva_one_shot_pin[] = {48, 46, 44, 42, 40, 38}; // selva_one_shot
int selva_one_shot_value[] = { 0, 0, 0, 0, 0, 0 };
int selva_sel_pin[] = { 52, 50, 36, 34 };
int selva_sel_value[] = { 0, 0, 0, 0 };

// SERES DE LA ISLA
int arp_led_pin = 39;
int arp_led_value = 0;
int arp_pin = 41;
int arp_value = 0;
int mic_pin = 35; // TODO
int mic_value = 0;
int seres_sel_pin[] = { 53, 51, 49, 47, 45, 43 };
int seres_sel_value[] = { 0, 0, 0, 0, 0, 0 };
int slide_ribbon_pin = A11;
int slide_ribbon_value = 0;
