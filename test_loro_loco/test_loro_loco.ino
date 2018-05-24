/*
 * RGB LED common anode means that anode is connected to 5V
 * and each color RGB to a resistor and to a analog output pin
 * then 255 in output means total oscurity
*/
int oscurity = 255;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by
int led_r = 3;
int led_g = 5;
int led_b = 6;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode( led_r, OUTPUT );
  pinMode( led_g, OUTPUT );
  pinMode( led_b, OUTPUT );
}

// the loop function runs over and over again forever
int i = 0;
int led_pin = 0 ;

void loop() {
 switch( i ) {
  case 0:  
    led_pin = led_r;
    break;
  case 1:  
    led_pin = led_g;
    break;
  case 2:  
    led_pin = led_b;
    break;
 }
  analogWrite( led_pin, oscurity );

  oscurity = oscurity - fadeAmount;
  if (oscurity <= 0 || oscurity >= 255) {
    fadeAmount = -fadeAmount;
    i++; if( i > 2) i = 0;
  }
  Serial.println(oscurity);
  delay(100);


}
