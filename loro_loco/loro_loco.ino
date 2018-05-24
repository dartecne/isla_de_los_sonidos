/*
 Name:		loro_loco.ino
 Created:	5/2/2018 2:42:03 PM
 Author:	locatis
*/

// the setup function runs once when you press reset or power the board
#include "loroLoco.h"
LoroLocoClass loro_loco;
void setup() {
	loro_loco.init();
	pinMode(13, OUTPUT);

}

// the loop function runs over and over again until power down or reset
void loop() {
	digitalWrite(13, 127);
	loro_loco.check_button();
	loro_loco.tick();
	delay(30);
}