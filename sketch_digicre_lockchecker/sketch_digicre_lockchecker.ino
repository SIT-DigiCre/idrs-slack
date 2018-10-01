int dKeyOut = 10;
int aKeyIn = 0;

void setup() {
  pinMode(dKeyOut, OUTPUT);
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
