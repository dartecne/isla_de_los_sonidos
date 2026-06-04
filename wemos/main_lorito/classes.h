#ifndef CLASSES_H
#define CLASSES_H

#define OSC_MSG_ROOT  "/lorito"
#define WIFI_SSID "LISA"
#define WIFI_PASS "lisa2025"

#define NUM_LEDS    24
#define BRIGHTNESS  120


IPAddress outIp(192,168,1,3); // Sonoron ethernet
//IPAddress outIp(192,168,1,10); // RaspPi
const unsigned int outPort = 8000;
//extern CRGB leds[NUM_LEDS];

class OSCManager {
public:
  WiFiUDP Udp;
  String str_bundle = OSC_MSG_ROOT;
  String str_msg_on = OSC_MSG_ROOT;
  String str_msg_off = OSC_MSG_ROOT;
  void begin() {
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
    
    Udp.begin(8888);
    str_bundle = str_bundle + "/";
    str_msg_on = str_msg_on + "/on";
    str_msg_off = str_msg_off + "/off";
    Serial.println(str_bundle.c_str());
  }
/** m - movement
    p - pitch
    r - roll
    pressure - presion del sensor de tacto
*/
  void sendValues(uint32_t m, uint32_t p, uint32_t r, uint32_t pressure) {
    OSCBundle bndl;
    bndl.add(str_bundle.c_str());
    bndl.add("/movement").add((uint32_t)m);
    bndl.add("/pitch").add((uint32_t)p);
    bndl.add("/roll").add((uint32_t)r);
    bndl.add("/pressure").add((uint32_t)pressure);
    Udp.beginPacket(outIp, outPort);
      bndl.send(Udp);
     Udp.endPacket();
    bndl.empty();
  }

  void sendOn(unsigned int val) {
    OSCMessage msg(str_msg_on.c_str());
    msg.add(val);
    Udp.beginPacket(outIp, outPort);
      msg.send(Udp);
    Udp.endPacket();
    msg.empty();
  }

  void sendOff(unsigned int val) {
    OSCMessage msg(str_msg_off.c_str());
    msg.add(val);
    Udp.beginPacket(outIp, outPort);
      msg.send(Udp);
    Udp.endPacket();
    msg.empty();
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
