//#include <WiFi.h>
#include <ESP8266WiFi.h>

#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include "classes.h"


OSCManager osc;
int i = 0;

void setup() {
  Serial.begin(115200);
  osc.begin(0);   // ID: lorito = 0
}

void loop() {
  osc.sendValues(i);
  i++;
  delay(100);
}

