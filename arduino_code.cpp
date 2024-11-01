#include <Servo.h>
const int servoCount = 4;
const int pwmPins[4] = {3,5,6,9};
Servo servo[servoCount];
#define STEP_PIN 11
#define DIR_PIN 10
String data;
int pos = 100;

void setup() 
{
  Serial.begin(115200);
  for (int i = 0; i<servoCount; i++) {
    servo[i].attach(pwmPins[i]);
  }
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
}
void  loop() {
  while (!Serial.available());
  data = Serial.readString();
  while (data.length() >= 3) {
    Serial.println(data);
    if (data.substring(0,1).toInt() == 5) {
      step(data.substring(1,4).toInt());
    } else {
      servo[data.substring(0,1).toInt()-1].write(data.substring(1,4).toInt());    
    }
    data = data.substring(4);
  }
}

void step(int go) {
  if (pos-go > 0) {
    digitalWrite(DIR_PIN, HIGH); // move forwards
  } else {
    digitalWrite(DIR_PIN, LOW); // move backwards
  }
  for (int i = 0; i < abs(pos-go); i++) { //move the difference
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(5000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(5000);
  }
  pos = go;
}