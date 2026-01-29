

#define TAU 20

void print_header() {
	Serial.println("Read Sensors and Print...");
	Serial.println("xa   ya   Dxa   Dya   xb   yb   Dxb   Dyb  IR  SW1  SW2  SW3  SW4  SW1_up SW2_up  SW3_up  SW4_up  SW1_down  SW2_down  SW3_down  SW4_down");
	Serial.println("----------------------------------------------------------------------------------------------------------------------------------------");
}

void send_int(int val) {
	Serial.write(0xff);
	Serial.write((val >> 8) & 0xff);
	Serial.write(val & 0xff);
}

void send_string(int val) {
	Serial.print(val, DEC);
	Serial.print(",");
	//  Serial.write( '\n0' );
}

void test_send_values() {
	for (int i = 0; i < 12; i++) {
		send_string(i);
	}
}

/*void send_sensor_values() {
	send_string(xa);
	send_string(ya);
	send_string(Dxa);
	send_string(Dya);
	send_string(xb);
	send_string(yb);
	send_string(Dxb);
	send_string(Dyb);
	send_string(IR);
	send_string(SW); // byte of switches
	send_string(SW_up); // byte of switches up
	Serial.println(SW_down, DEC); // byte of switches down
}*/
