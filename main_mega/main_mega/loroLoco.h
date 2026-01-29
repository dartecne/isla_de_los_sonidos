// loroLoco.h

#ifndef _LOROLOCO_h
#define _LOROLOCO_h



#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#define IDLE 0
#define REC 1
#define PLAY 2

#define PLAY_TIMER	3000
#define QUICK_FADE	14
#define SLOW_FADE	6

class LoroLocoClass
{
 protected:


 public:
	 int state = IDLE;
	 int oscurity = 0;
	 int fade_amount = SLOW_FADE;
	 unsigned long origin;
	 unsigned long present;
	 unsigned long timer = PLAY_TIMER; // ms of PLAY state

#ifdef PROTO
	 int led_r_pin = 12;
	 int led_g_pin = 13;
	 int one_shot = 26;
#else
	 int led_r_pin = 4;
	 int led_g_pin = 2;
	 int one_shot = 5;
#endif
	 int one_shot_led = 3;

	int one_shot_value = LOW;

	int check_button(); // checks if button is on and change state
	void reset_timer();
	bool check_timer(unsigned long timer);
	int tick(); // change leds ilumination
	void init();
	void test_leds();
};

extern LoroLocoClass LoroLoco;

#endif

