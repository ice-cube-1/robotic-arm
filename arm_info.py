import math
import serial
from time import sleep

def law_of_cosines(a: float, b: float, c: float) -> float:
    return math.acos((a * a + b * b - c * c) / (2 * a * b))

def distance(x: float, y: float) -> float:
    return math.sqrt(x * x + y * y)

class Beam:
    def __init__(self, length: float, absolute = 0.0):
        self.length = length
        self.absolute = absolute
        self.t: float = 0
        self.endx: float = 0
        self.endy: float = 0
        self.centerx: float = 0
        self.centery: float = length/2
        


class Arm:
    def __init__(self, beam0: Beam, beam1: Beam, beam2: Beam, beam3: Beam, clawOpen = 0) -> None:
        self.beam0 = beam0
        self.beam1 = beam1
        self.beam2 = beam2
        self.beam3 = beam3
        self.clawOpen = clawOpen
        self.arduino = serial.Serial('/dev/ttyUSB0', baudrate=115200)

    def setPosition(self, x: float, y: float) -> list[list[float]]:
        try:
            y = y-self.beam0.length
            x = x-self.beam3.length
            dist: float = distance(x, y)
            D1 = math.atan2(y, x)
            D2 = law_of_cosines(dist, self.beam1.length, self.beam2.length)
            self.beam1.t = D1 + D2
            self.beam1.absolute = self.beam1.t+math.radians(90)
            self.beam2.t = law_of_cosines(self.beam1.length, self.beam2.length, dist)
            self.beam2.absolute = (self.beam1.absolute+self.beam2.t)-math.radians(180)
            self.beam1.endx = self.beam1.length * math.cos(self.beam1.t)
            self.beam1.endy = self.beam1.length * math.sin(self.beam1.t)+self.beam0.length
            self.beam2.endx = self.beam1.endx - self.beam2.length * math.cos(self.beam1.t + self.beam2.t)
            self.beam2.endy = self.beam1.endy - self.beam2.length * math.sin(self.beam1.t + self.beam2.t)
            self.beam1.centerx = (self.beam1.endx)/2
            self.beam1.centery = (self.beam1.endy+self.beam0.length)/2
            self.beam2.centerx = (self.beam1.endx+self.beam2.endx)/2
            self.beam2.centery = (self.beam1.endy+self.beam2.endy)/2
            self.beam3.centerx = (self.beam2.endx*2+self.beam3.length)/2
            self.beam3.centery = self.beam2.endy
            self.sendToArduino()
            return [[self.beam0.centerx, self.beam0.centery, self.beam0.absolute, self.beam0.length],
                  [self.beam1.centerx, self.beam1.centery, self.beam1.absolute, self.beam1.length],
                  [self.beam2.centerx, self.beam2.centery, self.beam2.absolute, self.beam2.length],
                  [self.beam3.centerx, self.beam3.centery, self.beam3.absolute, self.beam3.length],
                  [self.beam2.endx+self.beam3.length, self.beam2.endy]]
        except:
            return []
    
    def plotInfo(self) -> list[list[float]]:
        return [[0,0, self.beam1.endx, self.beam2.endx, self.beam2.endx+self.beam3.length], [0, self.beam0.length, self.beam1.endy, self.beam2.endy, self.beam2.endy]]
    
    def sendToArduino(self) -> None:
        angle1 = 135-int(math.degrees(self.beam1.t)+calcAdjustment(self.beam1.absolute))
        angle2 = 180-int(math.degrees(self.beam2.t)-45)
        angle3 = int(math.degrees(self.beam1.t+self.beam2.t)-90)
        self.arduino.write(bytes("1" + str(angle1).zfill(3) + "2" + str(angle2).zfill(3) + "3" + str(angle3).zfill(3) + "\n", 'utf-8'))

    def move_claw(self, claw_pos):
        self.clawOpen = claw_pos
        self.arduino.write(bytes("4" + str(claw_pos).zfill(3) + "\n", 'utf-8'))
        sleep(2)
        self.arduino.write(bytes("5020","utf-8"))
        
def calcAdjustment(beamAbs: float) -> float:
    if (beamAbs < 0):
        print((-180-math.degrees(beamAbs))/20)
        return (-180-math.degrees(beamAbs))/20
    else: 
        print((-180-math.degrees(beamAbs))/20)
        return (180-math.degrees(beamAbs))/20