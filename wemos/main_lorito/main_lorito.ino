/**
  main_lorito - programa para el loro de peluche que incluye:
  -accelerometro MPU6050
  - anillo neopixel
  - sensor velostat

  Envia OSC con los siguientes datos:
  - Continuo: nivel de movimiento del gyro
  - Continuo: angulos Roll y Pitch
*/

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
//#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#include "classes.h"

#define BANG_THRES  5.0 // [0.11 - 1.5] no-move, [1.5, 5.0] move; >5.0 bang
#define PRESSURE_THRES  512 // max in 1024

#define LED_PIN        0 // ledRing GPIO0 is D3 
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

//Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

Adafruit_MPU6050 mpu;

CRGB leds[NUM_LEDS];

DualChaseEffect chase(
  6,              // longitud cola
  50,             // velocidad
  CRGB::Red,
  CRGB::Blue
);

SparkleEffect sparkles(
  50,             // probabilidad
  25,             // fade
  25              // intervalo
);

//Adafruit_Sensor *mpu_temp, *mpu_accel, *mpu_gyro;
sensors_event_t a, g, temp;
float pitch, roll, movement = 0;
unsigned int pressure = 0; // sensor de presión velostat


OSCManager osc;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); 

  Serial.println("Lorito Main");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  //setupt motion detection
  mpu.setHighPassFilter(MPU6050_HIGHPASS_0_63_HZ);
  mpu.setMotionDetectionThreshold(1);
  mpu.setMotionDetectionDuration(20);
  mpu.setInterruptPinLatch(true);	// Keep it latched.  Will turn off when reinitialized.
  mpu.setInterruptPinPolarity(true);
  mpu.setMotionInterrupt(true);

  mpu.getEvent(&a, &g, &temp);

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds,NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  
  osc.begin(0);

  Serial.println("setup OK");
  colorWipe(leds, CHSV(0,255,255), 50);
  randomSeed(analogRead(0));
  
  delay(100);
}

void loop() {
  fadeToBlackBy(leds, NUM_LEDS, 20);
  pressure = analogRead( A0 );
  Serial.println( pressure );
  double a_m = getAccMedia();
  Serial.println( a_m );
  getPitchRoll();
  
  int m = map(a_m, 0, 7, 0, 127);
  m = constrain( m, 0, 127 ); 
  int p = map(pitch, -180, 180, 0, 127);
  p = constrain( p, 0, 127 ); 
  int r = map(roll, -180, 180, 0, 127);
  r = constrain( r, 0, 127 );

  osc.sendValues(m, p, r, pressure);
  unsigned int mov = detectBang(a_m);
  if( mov > 0 ) osc.sendOn(mov);
  if(pressure > PRESSURE_THRES) osc.sendOn(pressure - PRESSURE_THRES);

//  chase.update(leds);
  sparkles.setDensity(map(m, 0,127, 10, 100));
  sparkles.setSpeed(map(pressure, 0, 1024, 10, 100));
  sparkles.update(leds);

  FastLED.show();

  delay(10);
}

void colorWipe( CRGB* leds, fl::CHSV color, int wait) {
  for(int i=0; i < NUM_LEDS; i++) { // For each pixel in strip...
    leds[i] = color;         //  Set pixel's color (in RAM)
    FastLED.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

void getPitchRoll() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float Ax = a.acceleration.x / 9.81;
  float Ay = a.acceleration.y / 9.81;
  float Az = a.acceleration.z / 9.81;
  float pitchRAW = atan2(Ax, Az) * 180 / M_PI;
  float rollRAW = atan2(Ay, Az) * 180 / M_PI;

  pitch = .25 * pitch + .75 * pitchRAW;
  roll = .25 * roll + .75 * rollRAW;

}

double getAccMedia() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  double a_m = g.gyro.x*g.gyro.x + g.gyro.y*g.gyro.y + g.gyro.z*g.gyro.z;
  return sqrt(a_m);
} 

unsigned int detectBang(double acc) {
  if(acc > BANG_THRES) return (acc - BANG_THRES);
  return 0;
}

void printIMUvalues() {
    /* Print out the values */
    Serial.print("AccelX:");
    Serial.print(a.acceleration.x);
    Serial.print(",");
    Serial.print("AccelY:");
    Serial.print(a.acceleration.y);
    Serial.print(",");
    Serial.print("AccelZ:");
    Serial.print(a.acceleration.z);
    Serial.print(", ");
    Serial.print("GyroX:");
    Serial.print(g.gyro.x);
    Serial.print(",");
    Serial.print("GyroY:");
    Serial.print(g.gyro.y);
    Serial.print(",");
    Serial.print("GyroZ:");
    Serial.print(g.gyro.z);
    Serial.println("");

}