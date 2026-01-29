#include <Adafruit_NeoPixel.h>
#include "clases.h"

#define PIXEL_PIN    5    
#define PIXEL_TUNEL_PIN    3    
#define PIXEL_COUNT 128
#define PIXEL_TUNEL_COUNT 80
#define NUM_GOTAS 12

#define VOLCAN_STRIP  1
#define TUNEL_STRIP  2

byte Gota::shape[5]= {255, 100, 6, 2, 0};

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);
//Adafruit_NeoPixel strip_tunel = Adafruit_NeoPixel(PIXEL_TUNEL_COUNT, PIXEL_TUNEL_PIN, NEO_GRB + NEO_KHZ800);

//Gota g[NUM_GOTAS];

void setup() {
  Serial.begin(9600);
  Serial.print( "setup......" );
  randomSeed(analogRead(A0));
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  
  test_leds_3();
    
  turn_off();
/** /
  for(int i = 0; i < NUM_GOTAS; i++) {
    int t = random( 40, 300 );
    int r = random(0, 7 );
    g[i].begin( strip, r, 0, t );
  }
  Serial.println( "[OK]" );
  /**/
}

int w = 0;

void loop() {
 /* */
  int o = random( 0, 3 );
//  o = 3;
  int t; 
  int n;
  uint32_t c;
  switch(o) {
    case 0:
//    d =random
      rugido_volcan(40, 1, 2000);
      break;
    case 1:
      t = random( 10, 60 );    
      rainbow( t );
      n = random( 1, strip.numPixels() );
      break;
    case 2:
      t = random( 40, 200 );    
      c = wheel( random(0, 255) );
      n = random( 10, 60 );
      theaterChase( c, t, n );
      break;
    case 3:
      n = random( 1, strip.numPixels() );
      for( int i = 0; i < strip.numPixels(); i++ )  {
        int d = map(n, 1, strip.numPixels(), 200, 20);
        sparkling( n, d, VOLCAN_STRIP );
      }
      break;
  }
}

void rugido_volcan( int d, int paso, int end_delay ) {
  int STEPS = 12;
  uint32_t red = strip.Color( 127, 10, 10 );
  for( int j = 0; j < 255; j = j + paso ) {
    red = strip.Color( j, 0, 0 );
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor( i, red );
    }
    strip.show();
    delay( d );    
  }
  for( int j = 255; j > 0; j = j - paso ) {
    red = strip.Color( j, 3, 3 );
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor( i, red );
    }
    strip.show();
    delay( d );    
  }
  delay( end_delay );
}

int sparkling( int n, int d, int s ) {
  uint32_t white = strip.Color( 127, 127, 127 );
  int m = random(1, 12);
  for (int i=0; i < strip.numPixels(); i++) {
    if( random( n ) < ( n - m) )
      strip.setPixelColor( i, 0 );    
    else
      strip.setPixelColor( i, white );  
  }
  strip.show();
  delay( d );
}

void theaterChase(uint32_t c, uint8_t wait, int n) {
  for (int j=0; j < n; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

/*
int goteo_colores() {
  for(int i = 0; i < NUM_GOTAS; i++) {
    g[i].tick();
    if( g[i].n > g[i].N ) {
      int r = random(0, 7 );
      int t = random( 40, 300 );
      uint32_t  c = wheel(w);
      w = w + 8;
      if( w == 256 ) { 
        w = 0;
        return 0;
      }
      g[i].set_tempo( t );
      g[i].set_color( c );
      g[i].n = 0;
    }
  }  
  return 1;
}

int goteo_blanco() {
  uint32_t  c = strip.Color(127, 127, 127);
  for(int i = 0; i < NUM_GOTAS; i++) {
    g[i].set_color( c );
    g[i].tick();
    if( g[i].n > g[i].N ) {
      int r = random(0, 7 );
      int t = random( 40, 300 );
      w = w + 8;
      if( w == 256 ) { 
        return 0;
      }
      g[i].set_tempo( t );
      g[i].n = 0;
    }
  }  
  return 1;
}
*/
void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}


void test_leds_3() {
  for( uint16_t i=0; i < strip.numPixels(); i++ ) {
    strip.setPixelColor( i, strip.Color( 127, 127, 127 ) );
  }
  strip.show();
  delay(1000);
}


void turn_off() {
  for( uint16_t i = 0; i < strip.numPixels(); i++ ) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
    strip.show();
  }
}


// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

