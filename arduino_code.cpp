#include <Servo.h>
#include <Stepper.h>
const int servoCount = 4;
const int pwmPins[6] = {3,5,6,9,10,11};
Servo servo[servoCount];
Stepper stepper(200, 7, 8, 11, 12);
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
  if (data.substring(0,1).toInt() == 5) {
     stepper.step(data.substring(1).toInt());
  } else {
    servo[data.substring(0,1).toInt()-1].write(data.substring(1).toInt());    
  }
  Serial.println(data.toInt()+1);
}