/**
 main puente v6 - Adaptación de LUZ MADRID a LISA
 Cambiamos mensajes OSC por bundles.
 
*/

#include <FastLED.h>
#include <WiFi.h>
#include <WiFiUdp.h>
//#include <OSCMessage.h>
#include <OSCBundle.h>

#include "classes.h"
// ================= CONFIG =================

#define LED_PIN1 13
#define LED_PIN2 12
#define LED_PIN3 14
#define LED_PIN4 27
#define SENSOR_PIN 32

// num LEDs
#define NUM1 64
#define NUM2 170
#define NUM3 170
#define NUM4 170

#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
#define BRIGHTNESS 120
#define NUM_COLORS  6

#define NUM_PLATFORMS 6 // numero de plataformas 

#define ID_1 11790164 // 7380472
#define ID_2 1972824
#define ID_3 10738116
#define ID_4 10796908
#define ID_5 10553708
#define ID_6 10690616

//ESP32-D0WD-V3 Rev 301
#define ID_1B 7380472 
#define ID_2B 7389836
#define ID_3B 8615068
#define ID_4B 8617424
#define ID_5B 8612700
#define ID_6B 7373904

uint8_t id; // id de la plataforma

CRGB strip1[NUM1];
CRGB strip2[NUM2];
CRGB strip3[NUM3];
CRGB strip4[NUM4];

//CRGBPalette16 palette;
//CRGB baseColor[NUM_PLATFORMS] = {CRGB::AntiqueWhite, CRGB::Green3, CRGB::DarkRed,CRGB::AntiqueWhite, CRGB::Green3, CRGB::DarkRed};
CRGB strip_color[NUM_COLORS] = {CRGB::AntiqueWhite, CRGB::Chartreuse, CRGB::DarkRed, CRGB::Amethyst, CRGB::BlueViolet,CRGB::Crimson};
//uint8_t hue_color[NUM_PLATFORMS] = {0, 96, 128, 0, 96, 128};
//uint8_t sat_color[NUM_PLATFORMS] = {255, 200, 0, 255, 200, 0};
uint8_t hue_color = 30; // HUE_ORANGE   leds[i].setHue( 160);
uint8_t sat_color = 255; 
CHSV orange_color( hue_color, sat_color, 255); //  leds[i].setHSV()

OSCManager osc;
SystemState currentState = IDLE;
SystemState lastState = IDLE;

FireworkTransition firework;
Lightning lightning2, lightning3, lightning4;

unsigned int lastSensorValue = 0;
int delta = 0;
unsigned int zeroValue = 0; // valor de referencia cuando no hay nadie subido a la plataforma
unsigned int deltaThreshold = 300; // diferencia entre un valor y el anterior. Midel si hay un pulso (subida o bajada)
float deltaFactor = 3.5; // minDelta = deltaThresh, maxDelta = deltaThres * deltaFactor
unsigned int randomFactor = 2; // random value for speed
unsigned int pressedThreshold = 2100; // por debajo se considera que hay peso
unsigned int noPressedThreshold = 1500; // por encima, se considera que no hay peso 
    // Sin peso [2100, 2900]
    // Con peso [1500, 500]
bool note_on, note_off;

unsigned long init_time = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("setting up...");
  uint32_t chipID = getChipID();
  Serial.println((String) "I am chipID: " + chipID + " myID:" + id);

  FastLED.addLeds<LED_TYPE,LED_PIN1,COLOR_ORDER>(strip1,NUM1);
  FastLED.addLeds<LED_TYPE,LED_PIN2,COLOR_ORDER>(strip2,NUM2);
  FastLED.addLeds<LED_TYPE,LED_PIN3,COLOR_ORDER>(strip3,NUM3);
  FastLED.addLeds<LED_TYPE,LED_PIN4,COLOR_ORDER>(strip4,NUM3);
  FastLED.setBrightness(BRIGHTNESS);

  analogReadResolution(12);

  FastLED.setMaxPowerInVoltsAndMilliamps(5,10000);

//  fill_solid(strip1, NUM1, orange_color); // CRGB::DarkRed
  fill_solid(strip1, NUM1, CRGB::DarkRed); // 
  Serial.println("Calibrating...");
//  calibrate();
  Serial.print("zeroValue = " ); Serial.println( zeroValue );
  Serial.print("pressedThreshold = " ); Serial.println( pressedThreshold );
  osc.begin(id);
//  test_trigger();
  delay(1000);
}

void loop() {
  unsigned int val = analogRead( SENSOR_PIN );
  Serial.println(val); // [2500, 600] // sin peso, con peso
  delta = val - lastSensorValue;
//  Serial.println(delta); // [2500, 600] // sin peso, con peso
  unsigned int speed = map(abs(delta), deltaThreshold, deltaThreshold*deltaFactor, 0, 10);
//  osc.sendForce( val, note_on, note_off );

  // Cambios de estado
  if(val < noPressedThreshold) {
    currentState = T_1;
  } else if((val > pressedThreshold) & (currentState == T_1)) {
    currentState = T_2;
  } else if( currentState == T_2 && ((millis() - init_time) > TIME_STATE_T_2) ) {
    currentState = IDLE;
  }

  // acciones de transicion de estado
  if(currentState == T_1 && lastState == IDLE) {
      firework.start();
      note_on = 1;
      note_off = 0;
      osc.sendForce( val, note_on, note_off );
      Serial.print("delta = "); Serial.println(delta); 
      Serial.print("speed = "); Serial.println(speed); 

      lightning2.trigger( speed + (randomFactor - random(randomFactor)), randomBlueColor() );
      lightning3.trigger( speed + (randomFactor - random(randomFactor)), randomMarineColor() );
      lightning4.trigger( speed + (randomFactor - random(randomFactor)), randomOceanColor() );
      Serial.println("currentState: T_1. NOTE_ON");
  } else if(currentState == T_2 && lastState == T_1) {
      Serial.print("delta = "); Serial.println(delta); 
      Serial.print("speed = "); Serial.println(speed); 
      lightning2.trigger( speed + (randomFactor - random(randomFactor)), randomBlueColor() );
      lightning3.trigger( speed + (randomFactor - random(randomFactor)), randomMarineColor() );
      lightning4.trigger( speed + (randomFactor - random(randomFactor)), randomOceanColor() );
      init_time = millis();
      Serial.println("currentState: T_2. NOTE_OFF");

  } else if(currentState == IDLE && lastState == T_2) {
      note_on = 0;
      note_off = 1;
      osc.sendForce( val, note_on, note_off );
      Serial.println("currentState: IDLE ");
  }

  // acciones de estado
  int t = random(60,100);
//  fadeToBlackBy(strip2, NUM2, 80);
  fadeToBlackBy(strip2, NUM2, t);
  t = random(60,100);
  fadeToBlackBy(strip3, NUM3, t);
  t = random(60,100);
  fadeToBlackBy(strip4, NUM4, t);

  switch (currentState) {
  case IDLE:
    {
      uint8_t fadeVal = sin8(millis()/16);
      fill_solid(strip1, NUM1, CHSV(160,255,fadeVal));
      fill_solid(strip1, NUM1, CHSV(hue_color,sat_color,fadeVal));
      lightning2.update(strip2, NUM2);
      lightning3.update(strip3, NUM3);
      lightning4.update(strip4, NUM4);
    }
    break;
  case T_1:
    firework.sparkle(strip1, NUM1, val);
    if(abs(delta) > deltaThreshold) {
      Serial.print("delta = "); Serial.println(delta); // [2500, 600] // sin peso, con peso
      Serial.print("speed = "); Serial.println(speed); // [2500, 600] // sin peso, con peso
      lightning2.trigger( speed + (randomFactor - random(randomFactor)), randomBlueColor() );
      lightning3.trigger( speed + (randomFactor - random(randomFactor)), randomMarineColor() );
      lightning4.trigger( speed + (randomFactor - random(randomFactor)), randomOceanColor() );
    }
    lightning2.update(strip2, NUM2);
    lightning3.update(strip3, NUM3);
    lightning4.update(strip4, NUM4);
    break;
  case T_2:
    firework.update(strip1, NUM1);
    lightning2.update(strip2, NUM2);
    lightning3.update(strip3, NUM3);
    lightning4.update(strip4, NUM4);
    break;
  }
  FastLED.show();
  lastState = currentState;
  lastSensorValue = val;
  delay( 10 );
}

void test_trigger() {
  long t = millis();
  int val = 0;
  while( val <= 10 ) {
    fadeToBlackBy(strip2, NUM2, 80);
    if( millis() - t > 1000) {
      Serial.println(val);
      lightning2.trigger( 2, (10 - val), strip_color[random(NUM_COLORS)] );
      t = millis();
      val++;
    }
    lightning2.update( strip2, NUM2 );
    FastLED.show();
  }
}
CRGB randomOceanColor() {
    uint8_t hue;

    switch (random8(3)) {
        case 0:
            hue = random8(150, 165);   // Azul claro
            break;
        case 1:
            hue = random8(165, 180);   // Azul medio
            break;
        default:
            hue = random8(180, 191);   // Azul marino
            break;
    }

    return CHSV(
        hue,
        random8(200, 256),
        random8(60, 256)
    );
}

CRGB randomMarineColor() {
    uint8_t hue = random8(165, 186);   // Azul intenso a azul marino
    uint8_t sat = random8(220, 256);   // Muy saturado
    uint8_t val = random8(40, 180);    // Brillo moderado

    return CHSV(hue, sat, val);
}

CRGB randomBlueColor() {
    // En FastLED:
    // 160 ≈ azul
    // 170-190 ≈ azul oscuro / marino
    // 192 ≈ violeta

    uint8_t hue = random8(150, 191);   // Solo tonos azules
    uint8_t sat = random8(180, 256);   // Alta saturación
    uint8_t val = random8(80, 256);    // Brillo variable

    return CHSV(hue, sat, val);
}

unsigned int calibrate() {
  uint8_t nValues = 16;

  for( int i = 0; i < nValues; i++ ) {
    zeroValue += analogRead(SENSOR_PIN);
    delay(10);
  }
  zeroValue = zeroValue / nValues;
  pressedThreshold = zeroValue - zeroValue / 4; // 
  return zeroValue;
}

uint32_t getChipID() {
  uint32_t chipID;
  for (int i = 0; i < 17; i = i + 8) {
    chipID |= ((ESP.getEfuseMac() >> (40 - i)) & 0xff) << i; 
  }
  Serial.printf("ESP32 Chip model = %s Rev %d\n", ESP.getChipModel(), ESP.getChipRevision());
  Serial.printf("This chip has %d cores\n", ESP.getChipCores());
  if(chipID == ID_1 | chipID == ID_1B) id = 0;
  else if(chipID == ID_2 | chipID == ID_2B) id = 1;
  else if(chipID == ID_3 | chipID == ID_3B) id = 2;
  else if(chipID == ID_4 | chipID == ID_4B) id = 3;
  else if(chipID == ID_5 | chipID == ID_5B) id = 4;
  else if(chipID == ID_6 | chipID == ID_6B) id = 5;
  else id = (int)random(1,NUM_PLATFORMS);

  return chipID;
}



