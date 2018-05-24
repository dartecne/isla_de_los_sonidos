/*
 test_leds
 test fade in 5 leds
*/

#include "Header.h"

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

int led_pin[] = {5, 6, 9, 10, 11};
int led_value[] = { 0,0,0,0,0};
int ball_led_pin = 8;
int ball_led_value = 0;
int selector_pin[] = {52, 50, 48, 46, 44, 42};
int selector_value[] = { 0,0,0,0,0,0 };
int pot_pin[] = {0, 1, 2, 3};
int pot_value[] = { 0, 0, 0, 0 };
int sw_pin[] = {2, 3, 4};
int sw_value[] = { 0, 0, 0 };
int piezo_pin[] = {10, 11, 12, 13, 14, 15}; // analog inputs
int piezo_value[] = { 0, 0, 0, 0, 0, 0}; // analog inputs
int sonar_pin = 8;	// digital i/o
long sonar_value = 0;	
int acc_pin[] = {8, 9}; // acelerometer axis
int acc_value[] = { 0, 0 }; 

void setup() {
  Serial.begin( 9600 );

  for( int i = 0; i < 5; i++ ) {
     brightness[i] = 0;
     pinMode( led_pin[i], OUTPUT );  
  }

  pinMode( ball_led_pin, OUTPUT );

  for( int i = 0; i < 6; i++ ) {
	 pinMode( selector_pin[i], INPUT );
  }

  for( int i = 0; i < 3; i++ ) {
    pinMode( sw_pin[i], INPUT );
  }
}


void loop() {
	for ( int i = 0; i < 6; i++ ) selector_value[i] = digitalRead( selector_pin[i] );
	for ( int i = 0; i < 4; i++ ) pot_value[i] = analogRead( pot_pin[i] );
	for ( int i = 0; i < 3; i++ ) sw_value[i] = digitalRead( sw_pin[i] );
	for ( int i = 0; i < 5; i++ ) piezo_value[i] = digitalRead( piezo_pin[i] );
	sonar_value = readDistance( sonar_pin );
	for ( int i = 0; i < 2; i++ ) acc_value[i] = digitalRead( acc_pin[i] );
  
  delay(30);
 }

int get_selection( int selector_value[] ) {
	for (int i = 0; i < 6; i++ ) {
		if (selector_value[i]) return i;
	}
}
 
long readDistance(int pin) {
	pinMode(pin, OUTPUT);
	digitalWrite( pin, LOW );
	delayMicroseconds( 2 );
	digitalWrite(pin, HIGH);
	delayMicroseconds( 5 );
	digitalWrite(pin, LOW);
	pinMode(pin, INPUT);
	long duration = pulseIn( pin, HIGH );
	return duration / 29 / 2;
}
