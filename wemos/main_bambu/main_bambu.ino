/**
  Programa principal para recoger el movimiento de los bambus y producir movimientos LED
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
uint8_t id; // id de la plataforma
unsigned int movement = 0;
unsigned int last_mov = 0;
int readings[NUM_VALUES];
int i = 0;
unsigned int mov_total = 0;
unsigned int mov_mean = 0;


OSCManager osc;
CRGB leds[NUM_LEDS];


DualChaseEffect chase(
  6,              // longitud cola
  50,             // velocidad
  CRGB::Red,
  CRGB::Blue
);

SparkleEffect sparkles(
  70,             // probabilidad
  25,             // fade
  12              // intervalo
);

void setup() {
  Serial.begin(115200);
  Serial.println("STONE...");
  uint32_t chipID = getChipID();
  Serial.println((String) "I am chipID: " + chipID + " myID:" + id);
//  analogReadResolution(12);
  osc.begin(id);
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds,NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  colorWipe(leds, CHSV(0,255,255), 50);
  randomSeed(analogRead(0));
  last_mov = analogRead(0);
  Serial.println("setup STONE OK");
}

void loop() {
  fadeToBlackBy(leds, NUM_LEDS, 20);
  movement = analogRead(0);
//  Serial.println( movement );
  osc.sendValues( movement );
  
  mov_total -= readings[i];
  readings[i] = last_mov - movement;
  last_mov = movement;
  readings[i] = abs(readings[i]);
  mov_total += readings[i];
  i++;
  if(i >= NUM_VALUES) i = 0;
  mov_mean = mov_total / NUM_VALUES;
  Serial.println( mov_mean );

  sparkles.setDensity(map(mov_mean, 0,127, 10, 100));
  sparkles.update(leds);

  FastLED.show();
  delay(60);
}


void colorWipe( CRGB* leds, fl::CHSV color, int wait) {
  for(int i=0; i < NUM_LEDS; i++) { // For each pixel in strip...
    leds[i] = color;         //  Set pixel's color (in RAM)
    FastLED.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
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
