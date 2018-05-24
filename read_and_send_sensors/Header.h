

#define TAU 20

void send_int(int val) {
	Serial.write(0xff);
	Serial.write((val >> 8) & 0xff);
	Serial.write(val & 0xff);
}

void send_value(int val) {
	Serial.print(val, DEC);
	Serial.print(",");
	//  Serial.write( '\n0' );
}

void send_string(int val) {
	send_value(val);
//	Serial.println(val);
}

void test_send_values() {
	for (int i = 0; i < 12; i++) {
		send_string(i);
	}
}
