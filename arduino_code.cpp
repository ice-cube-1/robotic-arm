#include <Servo.h>
#include <math.h>
const int servoCount = 4;
const int pwmPins[6] = {3,5,6,9,10,11};
int currentPositions[6] = {0,0,0,0,0,0};
Servo servo[servoCount];
String data;

void setup() 
{
  Serial.begin(115200);
  for (int i = 0; i<servoCount; i++) {
    servo[i].attach(pwmPins[i]);
  }
}
void  loop() {
  while (!Serial.available());
  data = Serial.readString();
  int currentAngle = 0;
  int servoNumber = data.substring(0,1).toInt()-1;
  int pos = data.substring(1).toInt();
  for (int i = 0; i<servoNumber; i++) {
    currentAngle += currentPositions[i];
  }
  servo[servoNumber].write(pos);
  delay(1000);
  int newData = -(abs(pos-45+currentAngle))/(0.5*(pos-45+currentAngle))+pos;
  if (pos == 45) {
    newData = 48;
  }
  servo[servoNumber].write(newData);
  Serial.println(newData);
  currentPositions[servoNumber] = pos;
}