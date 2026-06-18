/**
  Programa principal para recoger el movimiento de las piedras
  WEMOS D1 mini (clone)
*/
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <Wire.h>
//#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#include "classes.h"
#define NUM_VALUES  4
#define STILL_THRES 7 // menos de esto es reposo
#define MOV_THRES 10 // más de esto es movimiento

uint8_t id; // id de la plataforma
unsigned int movement = 0;
unsigned int last_mov = 0;
int readings[NUM_VALUES];
int i = 0;
unsigned int mov_total = 0;
unsigned int mov_mean = 0;
unsigned int last_mov_mean = 0;
bool on, off = 0;

OSCManager osc;

void setup() {
  Serial.begin(115200);
  Serial.println("STONE...");
  uint32_t chipID = getChipID();
  Serial.println((String) "I am chipID: " + chipID + " myID:" + id);
//  analogReadResolution(12);
  osc.begin(id);
  Serial.println("setup STONE OK");
}

void loop() {
  movement = analogRead(0);
//  Serial.println( movement );
  mov_total -= readings[i];
  readings[i] = last_mov - movement;
  last_mov = movement;
  readings[i] = abs(readings[i]);
  mov_total += readings[i];
  i++;
  if(i >= NUM_VALUES) i = 0;
  mov_mean = mov_total / NUM_VALUES;
  if( last_mov_mean <= STILL_THRES & mov_mean >= MOV_THRES ) {
    Serial.println( ">>>>BOOOM!!!" );
    on = 1;
    off = 0;    
  } else if( mov_mean <= STILL_THRES & last_mov_mean >= MOV_THRES ){
    Serial.println( "<<<<<SHHHH" );
    on = 0;
    off = 1;    
  }
  Serial.println( mov_mean );
  osc.sendValues( movement, mov_mean, on, off );
  on = 0;
  off = 0;
  last_mov_mean = mov_mean;
  delay(60);
}


uint32_t getChipID() {
  uint32_t chipID;
/**  for (int i = 0; i < 17; i = i + 8) {
    chipID |= ((ESP.getEfuseMac() >> (40 - i)) & 0xff) << i; 
  }
  Serial.printf("ESP32 Chip model = %s Rev %d\n", ESP.getChipModel(), ESP.getChipRevision());
  */
  chipID = ESP.getChipId();
  Serial.print("ID = "); Serial.println( chipID );

  if(chipID == ID_1 ) id = 0;
  else if(chipID == ID_2 ) id = 1;
  else if(chipID == ID_3 ) id = 2;
  else if(chipID == ID_4 ) id = 3;
  else if(chipID == ID_5 ) id = 4;
  else if(chipID == ID_6 ) id = 5;
  else id = (int)random(1,NUM_PLATFORMS);

  return chipID;
}
