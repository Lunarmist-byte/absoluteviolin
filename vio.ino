
/*
  Virtual Violin Controller
  Board: Arduino Nano
  Potentiometer middle pin: A0
  Serial baud rate: 115200
*/

const int POT_PIN = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int potValue = analogRead(POT_PIN);

  // Send a numeric reading for Python
  Serial.println(potValue);

  delay(5);
}
