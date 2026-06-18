/**
 main puente v6 - Adaptación de LUZ MADRID a LISA
 Cambiamos mensajes OSC por bundles.
 
*/

#include <FastLED.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>

#include "classes.h"
// ================= CONFIG =================

#define LED_PIN1 13
#define LED_PIN2 12
#define LED_PIN3 14
#define SENSOR_PIN 32

// num LEDs
#define NUM1 64
#define NUM2 170
#define NUM3 170

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

//CRGBPalette16 palette;
//CRGB baseColor[NUM_PLATFORMS] = {CRGB::AntiqueWhite, CRGB::Green3, CRGB::DarkRed,CRGB::AntiqueWhite, CRGB::Green3, CRGB::DarkRed};
CRGB strip_color[NUM_COLORS] = {CRGB::AntiqueWhite, CRGB::Chartreuse, CRGB::DarkRed, CRGB::Amethyst, CRGB::BlueViolet,CRGB::Crimson};
//uint8_t hue_color[NUM_PLATFORMS] = {0, 96, 128, 0, 96, 128};
//uint8_t sat_color[NUM_PLATFORMS] = {255, 200, 0, 255, 200, 0};
uint8_t hue_color = 30; // HUE_ORANGE   leds[i].setHue( 160);
uint8_t sat_color = 255; 
CHSV orange_color( hue_color, sat_color, 255); //  leds[i].setHSV()

QueueHandle_t eventQueue;
QueueHandle_t sensorValueQueue;

OSCManager osc;
SystemEvent ev;
SystemState currentState = IDLE;

FireworkTransition firework;
Lightning lightning2, lightning3;

int lastSensorValue = 0;
unsigned int zeroValue = 0; // valor de referencia cuando no hay nadie subido a la plataforma
unsigned int deltaThreshold = 300; // diferencia entre un valor y el anterior. Midel si hay un pulso (subida o bajada)
unsigned int pressedThreshold = 0; // umbral 

unsigned long init_time = 0;


// ================= SENSOR TASK =======================

void sensorTask(void *pvParameters) {
  osc.begin(id);
  while (true) {
    unsigned int val = analogRead(SENSOR_PIN);
    Serial.println(val);
    int delta = val - lastSensorValue;
    osc.sendForce( val );
    if( sensorValueQueue != NULL && uxQueueSpacesAvailable(sensorValueQueue) > 0 ) {
      int ret = xQueueSend(sensorValueQueue, (void*)&val, 0);
        if (ret == pdTRUE) {
          // The message was successfully sent.
        } else if (ret == errQUEUE_FULL) {
          Serial.println("Error sending sensorValueQueue");
        }  // Queue send check

    }
    if( abs(delta) > deltaThreshold ) { // Alguien se ha subido/bajado
      Serial.print("val = "); Serial.println(val);
      Serial.print("lastSensorValue = "); Serial.println(lastSensorValue);
      Serial.print("delta = "); Serial.println(delta);
      SystemEvent ev;
      ev.delta = delta;
      ev.force = val;
      
      if( delta > 0 ) osc.sendOn( ev.force ); // se ha subido
      else osc.sendOff(ev.force);             // se ha bajado

      Serial.println("Pressed: " + String(val));
      xQueueSend(eventQueue, &ev, portMAX_DELAY);
    }
    lastSensorValue = val;
    vTaskDelay( 40 / portTICK_PERIOD_MS ); // 20ms
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("setting up...");
  uint32_t chipID = getChipID();
  Serial.println((String) "I am chipID: " + chipID + " myID:" + id);

  FastLED.addLeds<LED_TYPE,LED_PIN1,COLOR_ORDER>(strip1,NUM1);
  FastLED.addLeds<LED_TYPE,LED_PIN2,COLOR_ORDER>(strip2,NUM2);
  FastLED.addLeds<LED_TYPE,LED_PIN3,COLOR_ORDER>(strip3,NUM3);
  FastLED.setBrightness(BRIGHTNESS);

  analogReadResolution(12);
  eventQueue = xQueueCreate(10, sizeof(SystemEvent));
  sensorValueQueue = xQueueCreate( 10, sizeof(unsigned int) );

  FastLED.setMaxPowerInVoltsAndMilliamps(5,10000);

//  fill_solid(strip1, NUM1, orange_color); // CRGB::DarkRed
  fill_solid(strip1, NUM1, CRGB::DarkRed); // 
  Serial.println("Calibrating...");
  calibrate();
  Serial.print("zeroValue = " ); Serial.println( zeroValue );
  Serial.print("pressedThreshold = " ); Serial.println( pressedThreshold );
  delay(1000);

  xTaskCreatePinnedToCore(
    sensorTask,
    "SensorTask",
    4000,
    NULL,
    1,
    NULL,
    1
  );
}

void loop() {
  SystemEvent ev;
  unsigned int val = 0; // sensor value
  if (xQueueReceive(eventQueue, &ev, 0) == pdPASS) {
    Serial.print("lastState: "); Serial.println(currentState);
    if ((ev.delta < 0) && currentState == IDLE) { // alguien sube
      currentState = T_1;
      firework.start();
      val = ev.force;
      lightning2.trigger( val + random(val/20), strip_color[random(NUM_COLORS)] );
      lightning3.trigger( val - random(val/20), strip_color[random(NUM_COLORS)] );
      Serial.println("currentState: T_1 ");
    }
    else if ((ev.delta > 0) && currentState == T_1) { // alguien baja
      currentState = T_2;
      val = ev.force;
      lightning2.trigger( val + random(val/20), strip_color[random(NUM_COLORS)] );
      lightning3.trigger( val - random(val/20), strip_color[random(NUM_COLORS)] );
      init_time = millis();
      Serial.println("currentState: T_2");
//      Serial.println(init_time);
    }
  } else if( currentState == T_2 && ((millis() - init_time) > TIME_STATE_T_1) ) {
      currentState = IDLE;
      Serial.println("currentState: IDLE ");
  //    Serial.println(millis());
  //    Serial.println(init_time);
  }

  fadeToBlackBy(strip2, NUM2, 80);
  fadeToBlackBy(strip3, NUM2, 80);

  switch (currentState) {
    case IDLE:
      {
        uint8_t fadeVal = sin8(millis()/16);
//        fill_solid(strip1, NUM1, CHSV(160,255,fadeVal));
        fill_solid(strip1, NUM1, CHSV(hue_color,sat_color,fadeVal));
        lightning2.update(strip2, NUM2);
        lightning3.update(strip3, NUM3);
      }
      break;

    case T_1:
      if (xQueueReceive(sensorValueQueue, &val, 0) == pdPASS) {
        firework.sparkle(strip1, NUM1, val);
      }  
      lightning2.update(strip2, NUM2);
      lightning3.update(strip3, NUM3);
      break;
    case T_2:
      firework.update(strip1, NUM1);
      lightning2.update(strip2, NUM2);
      lightning3.update(strip3, NUM3);
      break;
  }
  FastLED.show();
  delay( 10 );
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



