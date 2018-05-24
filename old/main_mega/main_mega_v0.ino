/*
test_leds
test fade in 5 leds
*/
#include "Header.h"

#define NUM_LEDS 6
#define NUM_CUEVA_SEL	3
#define NUM_SELVA_ONE_SHOT	6
#define NUM_SELVA_SEL	4
#define NUM_SW	6
#define NUM_SERES_SEL	6
#define NUM_PUENTE_PIEZOS	5

#define PS2CLOCK  D22
#define PS2DATA   D24

// PUENTE
int puente_piezo_pin[] = { A10, A11, A12, A13, A14, A15 }; // analog inputs
int puente_piezo_value[] = { 0, 0, 0, 0, 0, 0 }; // analog inputs

// TUNEL
int sonar_pin = D8;	// digital i/o
long sonar_value = 0;

// LOROLOCO
int loro_led_r_pin = D12;
int loro_led_g_pin = D13;
int loro_led_r_value = 0;
int loro_led_g_value = 0;
int loro_one_shot_pin = D26;
int loro_one_shot_value = 0;

//TIMON
int timon_data_value = 0;

// CUEVA DE LOS RUIDOS
int cueva_sel_pin[] = { D32, D30, D28 };
int cueva_sel_value[] = {0, 0, 0};
int sw_pin[] = { D23, D25, D27, D29, D31, D33 };
int sw_value[] = { 0, 0, 0, 0, 0, 0 };
int pot_pin[] = { A0, A1 };
int pot_value[] = { 0, 0 };
int led_pin[] = { D4, D5, D6, D9, D10, D11 };
int led_value[] = { 0, 0, 0, 0, 0 };

// SELVA SONIDOS AMBIENTE
int selva_one_shot_pin[] = { D44, D42, D40, D38, D36, D34 };
int selva_one_shot_value[] = { 0, 0, 0, 0, 0, 0 };
int selva_sel_pin[] = { D52, D50, D48, D46 };
int selva_sel_value[] = { 0, 0, 0, 0};
int joy_pin[] = { A8, A9 };
int joy_value[] = { 0, 0 };
int ball_led_pin = D7;
int ball_led_value = 0;

// SERES DE LA ISLA
int arp_led_pin = D39;
int arp_led_value = 0;
int arp_pin = D41;
int arp_value = 0;
int seres_sel_pin[] = { D53, D51, D49, D47, D45, D43 };
int slide_ribbon_pin[] = { A2, A3 };
int slide_ribbon_value[] = { 0, 0 };

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

/* Configuracion de
	PUENTE
	TUNEL
	LORO
	TIMON
	SERES ISLA
	CUVA RUIDOS
	SELVA_AMBIENTE

*/
void setup() {
	Serial.begin(9600);

	// PUENTE	
	// TUNEL

	// LORO
	pinMode( loro_led_r_pin, OUTPUT );
	pinMode( loro_led_g_pin, OUTPUT );
	pinMode( loro_one_shot_led_pin, OUTPUT );
	pinMode( loro_one_shot_pin, INPUT );

	// TIMON
	PS2GoHi(PS2CLOCK);
	PS2GoHi(PS2DATA);

	// SERES ISLA
	pinMode( arp_led_pin, OUTPUT );
	pinMode( arp_pin, INPUT );

	for (int i; i < NUM_SERES_SEL; i++ ) {
		pinMode( seres_sel_pin[i], INPUT );
	}

	// CUEVA RUIDOS
	for (int i = 0; i < NUM_LEDS; i++) {
		brightness[i] = 0;
		pinMode(led_pin[i], OUTPUT);
	}
	for (int i = 0; i < NUM_SW; i++) {
		pinMode(sw_pin[i], INPUT);
	}
	for (int i = 0; i < NUM_CUEVA_SEL; i++) {
		pinMode( cueva_sel_pin[i], INPUT);
	}
//
	test_leds();

	// SELVA AMBIENTE
	pinMode(ball_led_pin, OUTPUT);

	for (int i = 0; i < NUM_SELVA_SEL; i++) {
		pinMode(selva_sel_pin[i], INPUT);
	}

}

int T = 500; // periodo
int n = 0;
/*
  PUENTE
  TUNEL
  LORO
  TIMON
  SERES ISLA
  CUVA RUIDOS
  SELVA_AMBIENTE
*/

void loop() {
	// PUENTE
	for (int i = 0; i < NUM; i++) {
		puente_piezo_value[i]
	}

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
		analogWrite(led_pin[n_pin], led_value);
	}
	// TIMON
	PS2MousePos(stat, x, y);


	delay(20);
}

int get_selection() {
	for (int i = 0; i < 6; i++) {
		if (selector_value[i] == HIGH) return i;
	}
}

void turn_leds_off() {
	for (int i = 0; i < NUM_LEDS; i++) {
		analogWrite(led_pin[i], LOW);
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


void PS2GoHi(int pin) {
	pinMode(pin, INPUT);
	digitalWrite(pin, HIGH);
}

void PS2GoLo(int pin) {
	pinMode(pin, OUTPUT);
	digitalWrite(pin, LOW);
}

void PS2Write(unsigned char data) {
	unsigned char parity = 1;

	PS2GoHi(PS2DATA);
	PS2GoHi(PS2CLOCK);
	delayMicroseconds(300);
	PS2GoLo(PS2CLOCK);
	delayMicroseconds(300);
	PS2GoLo(PS2DATA);
	delayMicroseconds(10);
	PS2GoHi(PS2CLOCK);

	while (digitalRead(PS2CLOCK) == HIGH);

	for (int i = 0; i<8; i++) {
		if (data & 0x01) PS2GoHi(PS2DATA);
		else PS2GoLo(PS2DATA);
		while (digitalRead(PS2CLOCK) == LOW);
		while (digitalRead(PS2CLOCK) == HIGH);
		parity ^= (data & 0x01);
		data = data >> 1;
	}

	if (parity) PS2GoHi(PS2DATA);
	else PS2GoLo(PS2DATA);

	while (digitalRead(PS2CLOCK) == LOW);
	while (digitalRead(PS2CLOCK) == HIGH);

	PS2GoHi(PS2DATA);
	delayMicroseconds(50);

	while (digitalRead(PS2CLOCK) == HIGH);
	while ((digitalRead(PS2CLOCK) == LOW) || (digitalRead(PS2DATA) == LOW));

	PS2GoLo(PS2CLOCK);
}

unsigned char PS2Read(void) {
	unsigned char data = 0, bit = 1;

	PS2GoHi(PS2CLOCK);
	PS2GoHi(PS2DATA);
	delayMicroseconds(50);
	while (digitalRead(PS2CLOCK) == HIGH);

	delayMicroseconds(5);
	while (digitalRead(PS2CLOCK) == LOW);

	for (int i = 0; i<8; i++) {
		while (digitalRead(PS2CLOCK) == HIGH);
		if (digitalRead(PS2DATA) == HIGH) data |= bit;
		while (digitalRead(PS2CLOCK) == LOW);
		bit = bit << 1;
	}

	while (digitalRead(PS2CLOCK) == HIGH);
	while (digitalRead(PS2CLOCK) == LOW);
	while (digitalRead(PS2CLOCK) == HIGH);
	while (digitalRead(PS2CLOCK) == LOW);

	PS2GoLo(PS2CLOCK);

	return data;
}

void PS2MouseInit(void) {
	PS2Write(0xFF);
	for (int i = 0; i<3; i++) PS2Read();
	PS2Write(0xF0);
	PS2Read();
	delayMicroseconds(100);
}

void PS2MousePos(char &stat, char &x, char &y) {
	PS2Write(0xEB);
	PS2Read();
	stat = PS2Read();
	x = PS2Read();
	y = PS2Read();
}

