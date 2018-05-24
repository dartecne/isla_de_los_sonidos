/*
 test_leds
 test fade in 5 leds
*/

int brightness[5];    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
int led_pins[] = {5, 6, 9, 10, 11};
// the setup routine runs once when you press reset:
void setup() {
  for( int i = 0; i < 5; i++ ) {
    brightness[i] = 0;
    pinMode(led_pins[i], OUTPUT);  
  }
}

// the loop routine runs over and over again forever:
void loop() {
  for( int i = 0; i < 5; i++ ) {
    analogWrite(led_pins[i], brightness[0]);
  }
  brightness[0] = brightness[0] + fadeAmount;
  if (brightness[0] <= 0 || brightness[0] >= 255) {
    fadeAmount = -fadeAmount;
  }
  delay(30);
 }
