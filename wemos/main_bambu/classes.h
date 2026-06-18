#ifndef CLASSES_H
#define CLASSES_H

// numero de plataformas 
#define NUM_PLATFORMS 6 

#define ID_1 15498555
#define ID_2 6343916
#define ID_3 6278192
#define ID_4 6359693
#define ID_5 5
#define ID_6 6

#define OSC_MSG_ROOT  "/bambu/id"
#define WIFI_SSID "LISA"
#define WIFI_PASS "lisa2025"

#define NUM_LEDS    150
#define BRIGHTNESS  255

#define LED_PIN        2 // ledRing GPIO2 is D4 
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

#define BANG_THRES  5.0 // [0.11 - 1.5] no-move, [1.5, 5.0] move; >5.0 bang
#define PRESSURE_THRES  512 // max in 1024


IPAddress outIp(192,168,1,3); // Sonoron ethernet
//IPAddress outIp(192,168,1,10); // RaspPi
const unsigned int outPort = 8000;
//extern CRGB leds[NUM_LEDS];

class OSCManager {
public:
  WiFiUDP Udp;
  String str_bundle = OSC_MSG_ROOT;
  void begin( uint8_t id ) {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    for( int i = 0; i < 100; i++) {
      if( WiFi.status() != WL_CONNECTED ) {
        Serial.print(".");
        delay(100);
      } else {
        Serial.println("Connected!");
        break;
      }
    }
    if( WiFi.status() != WL_CONNECTED ) {
        Serial.println("ERROR Connecting to WiFi");
        return;
    }
    
    Udp.begin( 8888 );
    str_bundle = str_bundle + id + "/";
    Serial.println(str_bundle.c_str());
  }
/** m - movement
    p - pitch
    r - roll
    pressure - presion del sensor de tacto
*/
  void sendValues(uint32_t mov, uint32_t mov_mean, bool on, bool off) {
    OSCBundle bndl;
    bndl.add(str_bundle.c_str());
    bndl.add("/movement").add((uint32_t)mov);
    bndl.add("/mov_mean").add((uint32_t)mov_mean);
    bndl.add("/on").add((int32_t)on);
    bndl.add("/off").add((int32_t)off);
    Udp.beginPacket(outIp, outPort);
      bndl.send(Udp);
    Udp.endPacket();
    bndl.empty();
  }

};

// =====================================================
// EFECTO 1: DOBLE ROTACIÓN CON COLA
// =====================================================
class DualChaseEffect {
  private:
    uint8_t pos1 = 0;
    uint8_t pos2 = NUM_LEDS / 2;

    uint8_t tailLength;
    uint8_t speedMs;

    CRGB color1;
    CRGB color2;

    unsigned long lastUpdate = 0;

  public:
    DualChaseEffect(
      uint8_t tail = 5,
      uint8_t speed = 60,
      CRGB c1 = CRGB::Red,
      CRGB c2 = CRGB::Blue)
    {
      tailLength = tail;
      speedMs = speed;
      color1 = c1;
      color2 = c2;
    }

    void setSpeed(uint8_t speed) {
      speedMs = speed;
    }

    void update(CRGB* leds) {
      unsigned long now = millis();

      if (now - lastUpdate < speedMs)
        return;

      lastUpdate = now;

      // Dibujar cola del primer punto
      for (int i = 0; i < tailLength; i++) {
        int index = (pos1 - i + NUM_LEDS) % NUM_LEDS;
        uint8_t fade = map(i, 0, tailLength - 1, 255, 20);

        leds[index] += color1.nscale8(fade);
      }

      // Dibujar cola del segundo punto
      for (int i = 0; i < tailLength; i++) {
        int index = (pos2 + i) % NUM_LEDS;
        uint8_t fade = map(i, 0, tailLength - 1, 255, 20);

        leds[index] += color2.nscale8(fade);
      }

      // Movimiento opuesto
      pos1 = (pos1 + 1) % NUM_LEDS;
      pos2 = (pos2 - 1 + NUM_LEDS) % NUM_LEDS;
    }
};


// =====================================================
// EFECTO 2: SPARKLES BLANCOS
// =====================================================
class SparkleEffect {
  private:
    uint8_t probability;
    uint8_t fadeAmount;
    unsigned long lastUpdate = 0;
    uint8_t intervalMs;

  public:
    SparkleEffect(
      uint8_t prob = 40,
      uint8_t fade = 40,
      uint8_t interval = 30)
    {
      probability = prob;
      fadeAmount = fade;
      intervalMs = interval;
    }

    void setSpeed(uint8_t speed) {
      intervalMs = speed;
    }

    void setDensity(uint8_t d) {
      probability = map(d, 0, 100, 0, 256);
    }


    void update(CRGB* leds) {
      unsigned long now = millis();

      if (now - lastUpdate < intervalMs)
        return;

      lastUpdate = now;

      // Fade global suave
      fadeToBlackBy(leds, NUM_LEDS, fadeAmount);

      // Sparkle aleatorio
      if (random8() < probability) {
        int pixel = random16(NUM_LEDS);
        leds[pixel] += CRGB::White;
      }
    }
};


#endif
