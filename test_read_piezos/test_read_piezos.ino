void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

int v[6];

void loop() {
  // put your main code here, to run repeatedly:
  for( int i = 0; i < 6; i++ ) {
    v[i] = analogRead(i);
    Serial.print( v[i] );
    Serial.print( ", " );
  }
  Serial.println();
  delay(100);
}
