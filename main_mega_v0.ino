/*
test_leds
test fade in 5 leds
*/
#include "Header.h"

#define NUM_LEDS 5

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

int led_pin[] = { 4, 5, 6, 8, 9, 10 };
int led_value[] = { 0,0,0,0,0 };
int ball_led_pin = 7;
int ball_led_value = 0;
int selector_pin[] = { 40, 50, 48, 46, 44, 42  };
int selector_value[] = { 0,0,0,0,0,0 };
int pot_pin[] = { 0, 1, 2, 3 };
int pot_value[] = { 0, 0, 0, 0 };
int sw_pin[] = { 2, 3, 4 };
int sw_value[] = { 0, 0, 0 };
int piezo_pin[] = { 10, 11, 12, 13, 14, 15 }; // analog inputs
int piezo_value[] = { 0, 0, 0, 0, 0, 0 }; // analog inputs
int sonar_pin = 7;	// digital i/o
long sonar_value = 0;
int acc_pin[] = { 8, 9 }; // acelerometer axis
int acc_value[] = { 0, 0 };

void setup() {
	Serial.begin(9600);

	for (int i = 0; i < NUM_LEDS; i++) {
		brightness[i] = 0;
		pinMode(led_pin[i], OUTPUT);
	}

	pinMode(ball_led_pin, OUTPUT);

	for (int i = 0; i < 6; i++) {
		pinMode(selector_pin[i], INPUT);
	}

	for (int i = 0; i < 3; i++) {
		pinMode(sw_pin[i], INPUT);
	}
	test_leds();
}

int T = 500; // periodo
int n = 0;

void loop() {
	for (int i = 0; i < 6; i++) {
		selector_value[i] = digitalRead(selector_pin[i]);
		send_string(selector_value[i]);
	}
	for (int i = 0; i < 4; i++) {
		pot_value[i] = analogRead(pot_pin[i]);
//		send_string(pot_value[i]);
	}
	for (int i = 0; i < 3; i++) {
		sw_value[i] = digitalRead(sw_pin[i]);
//		send_string(sw_value[i]);
	}
	for (int i = 0; i < 5; i++) {
		piezo_value[i] = digitalRead(piezo_pin[i]);
//		send_string(piezo_value[i]);
	}
	sonar_value = readDistance(sonar_pin);
	for (int i = 0; i < 2; i++) {
		acc_value[i] = digitalRead(acc_pin[i]);
//		send_string(acc_value[i]);
	}
  Serial.println();
	//LEDs
//	int led_value = 255 * (1 + sin(2 * PI * TAU * n / T)) / 2;
//	n++; if (n > T) n = 0;
	int led_value = 255;
	analogWrite(ball_led_pin, led_value);
//	if (sw_value[1]) analogWrite( led_pin[get_selection()], led_value );
	int n_pin = get_selection();
  turn_leds_off();
	if (sw_value[1] == HIGH) {
    analogWrite( led_pin[n_pin], led_value );
	}
	// LEDS
	
	delay(20);
}

int get_selection() {
	for (int i = 0; i < 6; i++) {
		if (selector_value[i] == HIGH ) return i;
	}
}

void turn_leds_off() {
    for( int i = 0; i < NUM_LEDS; i++ ) {
      analogWrite( led_pin[i], LOW );
    }  
}

long readDistance(int pin) {
	pinMode(pin, OUTPUT);
	digitalWrite(pin, LOW);
	delayMicroseconds(2);
	digitalWrite(pin, HIGH);
	delayMicroseconds(5);
	digitalWrite(pin, LOW);
	pinMode(pin, INPUT);
	long duration = pulseIn(pin, HIGH);
	return duration / 29 / 2;
}

void test_leds() {
	int d = 300;
	analogWrite(ball_led_pin, 255);
	delay(d);
	for (int i = 0; i < NUM_LEDS; i++) {
		analogWrite(led_pin[i], 255);
		delay(d);
	}
	analogWrite(ball_led_pin, 0);
  turn_leds_off(); 
}
