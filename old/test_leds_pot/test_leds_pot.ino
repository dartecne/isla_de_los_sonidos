/*
 test_leds pot
 test fade in 5 leds controlled pot
*/

#define TAU 20

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
int led_pins[] = {5, 6, 9, 10, 11};
int pot_pins[] = {0, 1, 2, 3};
int sw_pins[] = {2, 3, 4};

int pot_value[] = {0, 0, 0, 0, 0};

void setup() {
  for( int i = 0; i < 5; i++ ) {
    brightness[i] = 0;
    pinMode( led_pins[i], OUTPUT );  
  }
  for( int i = 0; i < 3; i++ ) {
    pinMode( sw_pins[i], INPUT );
  }
}


int T = 1000; // periodo
int n = 0;

void loop() {
  for( int  i = 0; i < 5; i++ ) {
    pot_value[i] = analogRead( pot_pins[i] );
  }
  double led_value = 255 * ( 1 + sin(2 * PI * TAU * n / T) ) / 2;
  analogWrite( led_pins[0], led_value );
  n++;
  if( n > T/TAU ) n = 0;
  delay( TAU );
 }
 
