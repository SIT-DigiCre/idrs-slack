#include <Wire.h>

int dKeyOut = 10;
int aKeyIn = 0;
int i2caddr = 0x08;

void setup() {
  pinMode(dKeyOut, OUTPUT);
  Wire.begin(i2caddr);
  Wire.onRequest(i2csend);
  Serial.begin(9600);
}

void loop() {
  int analogval = analogRead(aKeyIn);
  Serial.println(analogval);
  if (analogval < 600) {
    // locked
    digitalWrite(dKeyOut, LOW);
  } else {
    // unlocked
    digitalWrite(dKeyOut, HIGH);
  }
  delay(1000);
}

void i2csend() {
  Wire.write(analogRead(aKeyIn) >> 2);
}
