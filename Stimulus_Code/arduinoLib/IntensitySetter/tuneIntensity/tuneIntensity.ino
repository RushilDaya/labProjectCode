
String pin13= "";
String pin12= "";
String pin11= "";

void setup() {
  // set the three outputs to high
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(11,OUTPUT);
  digitalWrite(13,HIGH);
  digitalWrite(12,HIGH);
  digitalWrite(11,HIGH);
  pin13.reserve(20);
  pin12.reserve(20);
  pin11.reserve(20);
}

void loop() {
  // read the resistor levels
  // this will be mapped to an intensity.

  Serial.print("\n LED1 = ");
  Serial.print(analogRead(A1));
  delay(100);
  Serial.print("\n LED2 = ");
  Serial.print(analogRead(A2));
  delay(100);
  Serial.print("\n LED3 = ");
  Serial.print(analogRead(A3));
  delay(100);
  
}
