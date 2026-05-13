#ifndef CLASSES_H
#define CLASSES_H

#define WIFI_SSID "LISA"
#define WIFI_PASS "lisa2025"

#define MAX_LIGHTNINGS 16

#define RED CHSV(0,255,255)
#define GREEN CHSV(96,255,255)
#define WHITE CHSV(0,0,255)

IPAddress outIp(192,168,1,10);
const unsigned int outPort = 8000;

//enum SystemState { IDLE, T_1, ACTIVE, T_2 };
enum SystemState { IDLE, T_1 };

struct SystemEvent {
    int delta;
    unsigned int force;
};

extern unsigned int adaptiveThreshold;

class OSCManager {
public:
  WiFiUDP Udp;
  String str_msg = "/sensor/force/id";
  String str_msg_on = "/sensor/on/id";
  String str_msg_off = "/sensor/off/id";
  void begin( uint8_t id ) {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    // TODO: evitar bucle infinito
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(200);
    }
    Udp.begin(8888);
//    str_msg += "id";
    str_msg += id;
    str_msg_on += id;
    str_msg_off += id;
    Serial.println(str_msg.c_str());
    Serial.println("Connected!");
  }

  void sendForce(unsigned int val) {
    OSCMessage msg(str_msg.c_str());
    msg.add(val);
    Udp.beginPacket(outIp, outPort);
      msg.send(Udp);
    Udp.endPacket();
    msg.empty();
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
// ================= TRANSICIÓN ========================
// =====================================================

class FireworkTransition {
public:
  bool active = false;
  bool fadePhase = true;
  unsigned long startTime = 0;

  void start() {
    active = true;
    fadePhase = true;
    startTime = millis();
  }

  void update(CRGB* strip1, int NUM1) {
    if (!active) return;
    if (fadePhase) {
      float t = (millis() - startTime) / 1000.0;
      uint8_t v = constrain(t * 255, 0, 255);
//      Serial.println(v);
      fill_solid(strip1, NUM1, CRGB(v, v, v));

      if (t >= 1.0) {
        fadePhase = false;
        startTime = millis();
      }
    } else {
      fadeToBlackBy(strip1, NUM1, 40);
      float decay = 1.0 - ((millis() - startTime) / 2000.0);
      decay = constrain(decay, 0.0, 1.0);
      if (random8() < 200 * decay) {
        strip1[random(NUM1)] += CRGB::White;
      }
      if (decay <= 0.0) active = false;
    }
  }
};

class Bolt {
  public:
    float pos;
    float speed;
    int length;
    bool active = false;
    CRGB color;
    uint8_t brightness;
    Bolt() : pos(0), speed(0.12), length(3), 
            active(false){} //, color(CRGB::Blue){}                                                                                                                                                                                           
    void init(uint force, CRGB c) {
      pos = 0;
//      speed = random( 2, 16 ) / 10.0;
      speed = map(force, 0, adaptiveThreshold, 16, 2) / 8.0;
      speed = constrain(speed, 0.12, 2);
      Serial.println(String("Inicia un bolt de speed: ") + String(speed));
      active = true;
      brightness = 80;
      color = c;
    }

    void update( int numLeds ) {
      if ( active ) {
        pos += speed;
        if (pos >= numLeds) {
          active = false;
          Serial.println("Bolt llego" );
        }
      }
    }

    void render(CRGB* leds, int numLeds) {
      if(!active) return;
      int p = (int)pos;

      for (int i = 0; i < length; i++) {
        int idx = pos - i;
        if (idx >= 0 && idx < numLeds) {
//          uint8_t fade = 255 - i * 80;  // pequeña cola
          leds[idx] += color; //CRGB(0, 0, fade);
        }
      }
    }
};

class Lightning {
  private:
    Bolt bolts[MAX_LIGHTNINGS];
    unsigned long lastSpawn;
    unsigned long nextInterval;

    void render(CRGB* leds, int numLeds) {
      for (int i = 0; i < MAX_LIGHTNINGS; i++) {
        bolts[i].render(leds, numLeds);
      }
    }
  public:

    void trigger(int f, CRGB c) {
      Serial.println("Triggering a bolt...");
      for (int i = 0; i < MAX_LIGHTNINGS; i++) {
        Serial.println("Bolt id: " + String(i) + ", active:"+ String(bolts[i].active));
        if (!bolts[i].active) {
          bolts[i].init(f, c);
          break;
        }
      }
    }

    void update( CRGB* leds, int numLeds ) {
      for (int i = 0; i < MAX_LIGHTNINGS; i++) {
        bolts[i].update(numLeds);
      }
      render(leds, numLeds);
    }


    void clearAll() {
      for (int i = 0; i < MAX_LIGHTNINGS; i++) {
        bolts[i].active = false;
      }
    }

    bool isActive() {
      bool active = false;
      for (int i = 0; i < MAX_LIGHTNINGS; i++) {
        active = active | bolts[i].active;
      }
      return active;
    }
};

#endif