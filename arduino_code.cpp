#include <Servo.h>
const int servoCount = 4;
const int pwmPins[4] = {3,5,6,9};
Servo servo[servoCount];
#define STEP_PIN 10
#define DIR_PIN 11
String data;
int pos = 0;

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
    if (data.substring(0,1).toInt() == 5) {
      step(data.substring(1).toInt());
    } else {
      servo[data.substring(0,1).toInt()-1].write(data.substring(1).toInt());    
    }
    data = data.substring(4);
  }
}

void step(int go) {
  int stepCount = posMod(go - pos, 200);
  if (stepCount > 100) {
    digitalWrite(DIR_PIN, HIGH);
    stepCount = 200-stepCount;
  } else {    
    digitalWrite(DIR_PIN, LOW);
  }
  for (int i = 0; i < stepCount; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delay(3);
    digitalWrite(STEP_PIN, LOW);
    delay(3);
  }
  pos = go;
}
int posMod(int i, int n) {
  return (i % n + n) % n;
}
