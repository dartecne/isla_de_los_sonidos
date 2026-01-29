#pragma once

#define NUM_LEDS 6
#define NUM_CUEVA_SEL	3
#define NUM_SELVA_ONE_SHOT	6
#define NUM_SELVA_SEL	4
#define NUM_SW	6
#define NUM_SERES_SEL	6
#define NUM_PUENTE_PIEZOS	6

//TIMON
#define PS2CLOCK  24
#define PS2DATA   22

//#define BAUDRATE	57600
//#define BAUDRATE	9600
#define BAUDRATE	115200

// TUNEL
#ifdef PROTO												 
int sonar_pin = 8;	// digital i/o
#else
int sonar_pin = 13;	// digital i/o
#endif
long sonar_value = 0;


//TIMON
long timon_data_value = 0;

// CUEVA DE LOS RUIDOS
int cueva_sel_pin[] = { 32, 30, 28 };
int cueva_sel_value[] = { 0, 0, 0 };
int sw_pin[] = { 23, 25, 27, 29, 31, 33 };
int sw_value[] = { 0, 0, 0, 0, 0, 0 };
int pot_pin[] = { A0, A1 };
int pot_value[] = { 0, 0 };
#ifdef PROTO
int led_pin[] = { 4, 5, 6, 9, 10, 11 };
#else
int led_pin[] = { 6, 7, 8, 9, 10, 11 };
#endif

int led_value[] = { 0, 0, 0, 0, 0 };

// SELVA SONIDOS AMBIENTE

#ifdef PROTO
int selva_one_shot_pin[] = { 44, 42, 40, 38, 36, 34 };
#else
int selva_one_shot_pin[] = { 48, 46, 44, 42, 40, 38 };
#endif

int selva_one_shot_value[] = { 0, 0, 0, 0, 0, 0 };
#ifdef PROTO
int selva_sel_pin[] = { 52, 50, 48, 46 };
#else
int selva_sel_pin[] = { 52, 50, 36, 34 };
#endif
int selva_sel_value[] = { 0, 0, 0, 0 };
int joy_pin[] = { A8, A9 };
int joy_value[] = { 0, 0 };
#ifdef PROTO
int ball_led_pin = 7;
#else
int ball_led_pin = 12;
#endif
int ball_led_value = 0;

// SERES DE LA ISLA
int arp_led_pin = 39;
int arp_led_value = 0;
int arp_pin = 41;
int arp_value = 0;
int seres_sel_pin[] = { 53, 51, 49, 47, 45, 43 };
int seres_sel_value[] = { 0, 0, 0, 0, 0, 0 };
int slide_ribbon_pin[] = { A2, A3 };
int slide_ribbon_value[] = { 0, 0 };
