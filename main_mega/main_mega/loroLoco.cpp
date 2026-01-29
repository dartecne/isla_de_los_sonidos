// 
// 
// 

#include "loroLoco.h"

int LoroLocoClass::check_button()
{
	one_shot_value = digitalRead( one_shot );
	if (one_shot_value == HIGH && state == IDLE) {
	//	test_leds();
		state = REC;
		fade_amount = QUICK_FADE;
		return one_shot_value;
	} else if (one_shot_value == LOW && state == REC) {
		state = PLAY;
		fade_amount = 0;
		oscurity = 0;
		reset_timer();
		return one_shot_value;
	} else if ( check_timer( timer ) && state == PLAY) {
		state = IDLE;
		fade_amount = SLOW_FADE;
	}

	return one_shot_value;
}

void LoroLocoClass::reset_timer()
{
	present = origin;
	origin = millis();
}

bool LoroLocoClass::check_timer( unsigned long timer )
{
	present = millis();
	if (present - origin > timer) return true;
	return false;
}

// esta funcion mete ruido en el audio
int LoroLocoClass::tick()
{
	if (state == IDLE) {
		analogWrite( led_g_pin, oscurity );
		analogWrite( led_r_pin, 255);
    analogWrite(one_shot_led, oscurity);
	}
	else if ( state == REC ) {
//		analogWrite(led_g_pin, 255); 
//		analogWrite(led_r_pin, oscurity);
    digitalWrite(led_g_pin, HIGH); 
    digitalWrite(led_r_pin, LOW);
    return(0);
	}
	else if ( state == PLAY ) {
		analogWrite(led_g_pin, oscurity);
		analogWrite(led_r_pin, oscurity);
    analogWrite(one_shot_led, oscurity);
	}
	else {
		state = IDLE;
	}

	oscurity = oscurity + fade_amount;
//	oscurity = 0;
	if (oscurity <= 0 || oscurity >= 255) {
		fade_amount = -fade_amount;
		oscurity = constrain( oscurity, 0, 255 );
	}

	return 0;
}

void LoroLocoClass::init()
{
	pinMode( one_shot, INPUT );
	pinMode( one_shot_led, OUTPUT );
	pinMode( led_r_pin, OUTPUT );
	pinMode( led_g_pin, OUTPUT );
	state = IDLE;
	test_leds();
	origin = millis();

}
void LoroLocoClass::test_leds() {
	// eyes in green
	analogWrite( led_r_pin, 0);
	analogWrite( led_g_pin, 255);
	analogWrite( one_shot_led, 255 );
	delay(1000);
	// eyes in red
	analogWrite( led_r_pin, 255 );
	analogWrite( led_g_pin, 0 );
	analogWrite( one_shot_led, 0 );
	delay(1000);
}


LoroLocoClass LoroLoco;


