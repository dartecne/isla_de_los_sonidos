#include <Adafruit_NeoPixel.h>

class Gota {
  public:
  
    Gota(){};
    ~Gota(){};
    
  Adafruit_NeoPixel * strip;
  int n = 0; // position of Gota
  int tempo = 30; // time of each step in tick
  int len = 5;
  int N; // number of LEDs
  static byte shape[5];
  long millis_start = 0;
  uint32_t color;
  
  void begin( Adafruit_NeoPixel & strip, int branch_id, int n, int tempo) {
    this->strip = &strip;
    this->N = strip.numPixels();
    millis_start = millis();  
    this->tempo = tempo;
    this->n = n;
    color = white(127); 
  }
      
  void set_tempo( int tempo ) {
    this->tempo = tempo;
  }

  void set_color( uint32_t color ) {
    this->color = color;
  }

  void tick() {
    if( millis() - millis_start > tempo ) {
      if( n <= Gota::N + len ) {
        n = n + 1;
        draw(); 
        millis_start = millis();       
      }
    }
  }

  void draw() {
    for( int i = 0; i < len; i++ ) {
      int k = n - i; 
      k = constrain(k, 0, Gota::N);
//      strip->setPixelColor( j, white(Gota::shape[i]) );
      strip->setPixelColor( k, intensity(color, Gota::shape[i]) );
    }
    strip->show();
  }
  uint32_t white(uint32_t i) {
    i = constrain(i, 0, 255);
    return( strip->Color(i, i, i) );
  }
  
  uint32_t intensity( uint32_t c, uint32_t i ) {
    i = constrain(i, 0, 255);
    return(strip->Color(red(c) * i / 255, green(c) * i / 255, blue(c) * i / 255));    
  }
  
  uint8_t red( uint32_t c ) {
    return (c >> 16);
  }
  
  uint8_t green( uint32_t c ) {
    return (c >> 8);
  }
  
  uint8_t blue( uint32_t c ) {
    return (c);
  }
};

