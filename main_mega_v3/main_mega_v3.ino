/*
 main control of Isla de los Sonidos
 v.3 - actualización para el proyecto con la FECyT
 - Se quita el Loro Loco porque se va a hacer wireless con ESP32
 - Se quitan los piezos del puento porque se van a hacer wireless con ESP32

 configure leds and sensors

 read sensors
 send data via RX
 handle LEDs values

 format of data is:
 ...

 TODO:
 implement timeouts in PS2 readings

*/
//#define TIMON_ON
//#define TUNEL_ON
//#define PROTO

#include "Header.h" //with sonoron.sln this path is enough as VisualStudio gets the file
#include "definitions.h"


int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
int piezo_threshold = 120; // minimum value to detect a hit

unsigned long micros_start = 0L;
unsigned long bpm = 220UL; // Beats per Minute

int count = 0;
String data = "";

/* Configuracion de
TUNEL
TIMON
SERES ISLA
CUEVA RUIDOS
SELVA_AMBIENTE
*/

void setup() {
	Serial.begin( BAUDRATE );
	micros_start = micros();

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
	for (int i = 0; i < NUM_SELVA_SEL; i++) {
		pinMode(selva_sel_pin[i], INPUT);
	}
	test_leds();
}

int led_index = 0;

/*
TUNEL
TIMON
SERES ISLA
CUEVA RUIDOS
SELVA_AMBIENTE
*/

void loop() {

	// TUNEL
#ifdef TUNEL_ON
	sonar_value = readDistance(tunel_trigger, tunel_echo);
#else
	sonar_value = 0;
#endif

	send_string(sonar_value);

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

  mic_value= digitalRead( mic_pin);
  send_string(mic_value);

	for (int i = 0; i < NUM_SERES_SEL; i++) {
		seres_sel_value[i] = digitalRead( seres_sel_pin[i] );
		send_string(seres_sel_value[i]);
	}
	slide_ribbon_value = analogRead( slide_ribbon_pin );
	send_string( slide_ribbon_value );
  send_string( analogRead(A0)); // mandamos ruido
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
		int v = analogRead(A0); // mandamos ruido
		v = map(v, 0, 1023, 0, 127); // map for MIDI
		send_string(v);
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
	int v = analogRead(A0);
//	joy_value[0] = map(joy_value[0], 0, 1023, 0, 127); // map for MIDI
	send_string(v);
	send_string(v);

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
		send_string( led_index ); // PING to synchro arduino Sequencer with Python implementation

		micros_start = micros();
	}
	else {
		send_string(-1);  // index -1 when time hasn't arrive to tempo, yet.
	}
	send_string(Serial.availableForWrite());//	if (< 41) delay(1000);

	Serial.println(count);
	count++;
	
	int b = 0;
	while (Serial.available()); // waits data from python app
	do {
		b = Serial.read();

	} while (b != '<'); // signal that python app already read serial buffer. No data losed
	
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

long readDistance(int tri, int echo) {
	pinMode(tri, OUTPUT);
	digitalWrite(tri, LOW);
	delayMicroseconds(2);
	digitalWrite(tri, HIGH);
	delayMicroseconds(5);
	digitalWrite(tri, LOW);
	pinMode(echo, INPUT);
	long duration = pulseIn(echo, HIGH, 100000);
	return duration / 29 / 2;
}

void test_leds() {
	int d = 300;
	delay(d);
	for (int i = 0; i < NUM_LEDS; i++) {
		analogWrite(led_pin[i], 255);
		delay(d);
	}
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
