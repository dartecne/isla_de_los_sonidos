/*
 Name:		Sketch1.ino
 Created:	5/1/2018 10:50:33 AM
 Author:	locatis
*/

// the setup function runs once when you press reset or power the board
void setup() {
	Serial.begin(9600);
	Serial.println("test Ribbon ==============");
}

// the loop function runs over and over again until power down or reset
void loop() {
	int v = analogRead(0);
	Serial.println(v);
	delay(100);
  
}
