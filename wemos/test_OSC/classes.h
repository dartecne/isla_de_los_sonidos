#ifndef CLASSES_H
#define CLASSES_H

#define OSC_MSG_ROOT  "/lorito/id"
#define WIFI_SSID "LISA"
#define WIFI_PASS "lisa2025"

IPAddress outIp(192,168,1,3); // Sonoron ethernet
//IPAddress outIp(192,168,1,10); // RaspPi
const unsigned int outPort = 8000;

class OSCManager {
public:
  WiFiUDP Udp;
  String str_bundle = OSC_MSG_ROOT;
  String str_msg_on = OSC_MSG_ROOT;
  String str_msg_off = OSC_MSG_ROOT;
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
    
    Udp.begin(8888);
    str_bundle = str_bundle + id + "/";
    str_msg_on = str_msg_on + id + "/on";
    str_msg_off = str_msg_off + id + "/off";
    Serial.println(str_bundle.c_str());
  }

  void sendValues(unsigned int val) {
    OSCBundle bndl;
    bndl.add(str_bundle.c_str());
    bndl.add("/pitch").add((int32_t)64);
    bndl.add("/roll").add((int32_t)val);
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

#endif
