/*
 main control of Isla de los Sonidos
 v.0

 configure leds and sensors

 read sensors
 send data via RX
 handle LEDs values

 format of data is:
 ...

 TODO:
 implement timeouts in PS2 readings


*/
#include "loroLoco.h"

#include "Header.h"

//#define TIMON_ON
//#define TUNEL_ON

#define NUM_LEDS 6
#define NUM_CUEVA_SEL	3
#define NUM_SELVA_ONE_SHOT	6
#define NUM_SELVA_SEL	4
#define NUM_SW	6
#define NUM_SERES_SEL	6
#define NUM_PUENTE_PIEZOS	6

#define PS2CLOCK  24
#define PS2DATA   22

//#define BAUDRATE	57600
//#define BAUDRATE	9600
#define BAUDRATE	115200

// PUENTE
int puente_piezo_pin[] = { A10, A11, A12, A13, A14, A15 }; // analog inputs
int puente_piezo_value[] = { 0, 0, 0, 0, 0, 0 }; // analog inputs

												 // TUNEL
int sonar_pin = 8;	// digital i/o
long sonar_value = 0;

// LOROLOCO
LoroLocoClass loro_loco;

//TIMON
long timon_data_value = 0;

// CUEVA DE LOS RUIDOS
int cueva_sel_pin[] = { 32, 30, 28 };
int cueva_sel_value[] = { 0, 0, 0 };
int sw_pin[] = { 23, 25, 27, 29, 31, 33 };
int sw_value[] = { 0, 0, 0, 0, 0, 0 };
int pot_pin[] = { A0, A1 };
int pot_value[] = { 0, 0 };
int led_pin[] = { 4, 5, 6, 9, 10, 11 };
int led_value[] = { 0, 0, 0, 0, 0 };

// SELVA SONIDOS AMBIENTE
int selva_one_shot_pin[] = { 44, 42, 40, 38, 36, 34 };
int selva_one_shot_value[] = { 0, 0, 0, 0, 0, 0 };
int selva_sel_pin[] = { 52, 50, 48, 46 };
int selva_sel_value[] = { 0, 0, 0, 0 };
int joy_pin[] = { A8, A9 };
int joy_value[] = { 0, 0 };
int ball_led_pin = 7;
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

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
int piezo_threshold = 120; // minimum value to detect a hit

unsigned long micros_start = 0L;
unsigned long bpm = 220UL; // Beats per Minute

int count = 0;
String data = "";

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
	Serial.begin( BAUDRATE );
	micros_start = micros();

	// PUENTE	
	// TUNEL

	// LORO
	loro_loco.init();

	// TIMON
	PS2GoHi(PS2CLOCK);
	PS2GoHi(PS2DATA);

	// SERES ISLA
	pinMode(arp_led_pin, OUTPUT);
	pinMode(arp_pin, INPUT);

	for (int i; i < NUM_SERES_SEL; i++) {
		pinMode(seres_sel_pin[i], INPUT);
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
		pinMode(cueva_sel_pin[i], INPUT);
	}
	//

	// SELVA AMBIENTE
	pinMode(ball_led_pin, OUTPUT);

	for (int i = 0; i < NUM_SELVA_SEL; i++) {
		pinMode(selva_sel_pin[i], INPUT);
	}
	test_leds();
}

int led_index = 0;

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
	for (int i = 0; i < NUM_PUENTE_PIEZOS; i++) {
		puente_piezo_value[i] = analogRead( puente_piezo_pin[i] );
		send_string( puente_piezo_value[i] );
	}

	// TUNEL
#ifdef TUNEL_ON
	sonar_value = readDistance(sonar_pin);
#else
	sonar_value = 0;
#endif

	send_string(sonar_value);

	// LORO
	int loro_one_shot_value = loro_loco.check_button();
	loro_loco.tick();
	send_string(loro_one_shot_value);

	// TIMON
	char stat, x = 0, y;
#ifdef TIMON_ON
	PS2MousePos(stat, x, y);
	timon_data_value = x + '0' - 48;// no se porque hay un offset de 48
#else
	timon_data_value = 0;
#endif

	send_string(timon_data_value );

	/*TODO: gestionar el cambio en los BPMs de los LEDs*/

	// SERES ISLA
	arp_value = digitalRead( arp_pin );
	send_string(arp_value);

	if (arp_value == HIGH) digitalWrite( arp_led_pin, HIGH );
	else digitalWrite( arp_led_pin, LOW );

	for (int i = 0; i < NUM_SERES_SEL; i++) {
		seres_sel_value[i] = digitalRead( seres_sel_pin[i] );
		send_string(seres_sel_value[i]);
	}
	for (int i = 0; i < 2; i++) {
		slide_ribbon_value[i] = analogRead( slide_ribbon_pin[i] );
		send_string( slide_ribbon_value[i] );
	}

	//CUEVA RUIDOS
	for (int i = 0; i < NUM_CUEVA_SEL; i++) {
		cueva_sel_value[i] = digitalRead( cueva_sel_pin[i] );
		send_string( cueva_sel_value[i] );
	}
	for (int i = 0; i < NUM_SW; i++) {
		sw_value[i] = digitalRead( sw_pin[i] );
		send_string(sw_value[i]);
	}
	for (int i = 0; i < 2; i++) {
		pot_value[i] = analogRead(pot_pin[i]);
		send_string(pot_value[i]);
	}

	//SELVA_AMBIENTE
	for (int i = 0; i < NUM_SELVA_ONE_SHOT; i++) {
		selva_one_shot_value[i] = digitalRead( selva_one_shot_pin[i] );
		send_string(selva_one_shot_value[i]);
	}
	for (int i = 0; i < NUM_SELVA_SEL; i++) {
		selva_sel_value[i] = digitalRead( selva_sel_pin[i] );
		send_string(selva_sel_value[i]);
	}
	joy_value[0] = analogRead(joy_pin[0]);
	send_string(joy_value[0]);
	joy_value[1] = analogRead(joy_pin[1]);
	send_string(joy_value[1]);

//	analogWrite(ball_led_pin, brightness[0]);
	analogWrite(ball_led_pin, 255);

	/* handling rhythm leds */
	if (micros() < micros_start) {
		micros_start = micros();
	}

//	double tempo_float = 1000UL * 60UL / bpm;
//	unsigned long tempo = (unsigned long) tempo_float;
	bpm += timon_data_value;
	bpm = constrain( bpm, 0, 500 );
	unsigned long tempo = 1000000UL * 60UL / bpm;

	send_string( bpm );
	send_string( tempo );

	if ( micros() - micros_start > tempo ) {
		turn_leds_off();
		led_index++;
		if (led_index >= NUM_LEDS) led_index = 0;
		if (sw_value[led_index] == HIGH) analogWrite( led_pin[led_index], 255 );

		micros_start = micros();
	}
	send_string(Serial.availableForWrite());//	if (< 41) delay(1000);

	Serial.println(count);
	count++;
	
	int b = 0;
	while (Serial.available()); // waits data from python app
	do {
		b = Serial.read();

	} while (b != '<'); // signal that python app already read serial buffer. No data losed
	
	//while (Serial.availableForWrite() < 8);
//	Serial.print(tempo);
//	Serial.print(",");
//	Serial.println(bpm);

//	delay(40);
}

int get_selection( int sel_value[], int N ) {
	for (int i = 0; i < N; i++) {
		if (sel_value[i] == HIGH) return i;
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

	while (digitalRead(PS2CLOCK) == HIGH); // TODO: hacer que estas esperas "while" tenga un timeout

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

