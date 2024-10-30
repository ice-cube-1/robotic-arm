from camera import Camera
from time import sleep
from arm_info import Arm, Beam
import math
cam = Camera()
arm = Arm(Beam(59.5+4), Beam(67.6+4),Beam(70.6+4),Beam(25,math.radians(90)))
while True:
    move = cam.getCentral()
    if abs(move) <= 100: break
    arm.setStepper(arm.stepperPos-int(move/100))
    sleep(2)