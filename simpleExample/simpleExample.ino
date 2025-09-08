/*
  simpleExample

  Reads an analog input on pin 0, receives and converts serial characters to int and prints the result to the Serial Monitor.
  Corresponds to simple_config.txt 

*/

int sensorValue = 0;
int serialValue = 0;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  sensorValue = analogRead(A0);
  if (Serial.available()){
    serialValue = int(Serial.read());
  }
  //csv format print
  Serial.print(millis());
  Serial.print(",");
  Serial.print(serialValue);
  Serial.print(",");
  Serial.print(sensorValue);
  Serial.print("\n");
  delay(1);
}
