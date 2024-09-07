#include <Servo.h>
#include <math.h>
const int servoCount = 2;
const int pwmPins[6] = {3,5,6,9,10,11};
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
  servo[data.substring(0,1).toInt()-1].write(data.substring(1).toInt()*10/9);
  Serial.println(data.toInt());
}