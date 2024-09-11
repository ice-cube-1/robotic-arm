import math
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

    def setPosition(self, x: float, y: float) -> bool:
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
            print([[self.beam0.centerx, self.beam0.centery, self.beam0.absolute, self.beam0.length],
                  [self.beam1.centerx, self.beam1.centery, self.beam1.absolute, self.beam1.length],
                  [self.beam2.centerx, self.beam2.centery, self.beam2.absolute, self.beam2.length],
                  [self.beam3.centerx, self.beam3.centery, self.beam3.absolute, self.beam3.length]])
            print(math.degrees(self.beam0.absolute), math.degrees(self.beam1.absolute), math.degrees(self.beam2.absolute), math.degrees(self.beam3.absolute))
            return True
        except:
            return False
    
    def plotInfo(self) -> list[list[float]]:
        print([0,0, self.beam1.endx, self.beam2.endx, self.beam2.endx+self.beam3.length], [0, self.beam0.length, self.beam1.endy, self.beam2.endy, self.beam2.endy])
        return [[0,0, self.beam1.endx, self.beam2.endx, self.beam2.endx+self.beam3.length], [0, self.beam0.length, self.beam1.endy, self.beam2.endy, self.beam2.endy]]
    
    def sendToArduino(self) -> None:
        angle = 135-int(math.degrees(self.beam1.t))
        # arduino.write(bytes("1" + str(angle) + "\n", 'utf-8'))
        sleep(1)
        angle = 180-int(math.degrees(self.beam2.t)-30)
        # arduino.write(bytes("2" + str(angle) + "\n", 'utf-8'))
        sleep(1)
        angle = int(math.degrees(self.beam1.t+self.beam2.t)-90)
        # arduino.write(bytes("3" + str(angle) + "\n", 'utf-8'))
        print(angle)

    def move_claw(self):
        self.clawOpen = claw_pos.get()
        angle = self.clawOpen*90
        # arduino.write(bytes("4" + str(angle) + "\n", 'utf-8'))

def update():
    if arm.setPosition(float(xin.get()), float(yin.get())):
        data = arm.plotInfo()
        print(math.degrees(arm.beam0.absolute), math.degrees(arm.beam1.absolute), math.degrees(arm.beam2.absolute), math.degrees(arm.beam3.absolute))
        arm.sendToArduino()
        ax.clear()
        ax.plot(data[0], data[1])
        ax.set_xlim(-limit+arm.beam3.length, limit+arm.beam3.length)
        ax.set_ylim(0, limit+arm.beam0.length)
        canvas.draw()

arm = Arm(Beam(59.5), Beam(67.6),Beam(67.6),Beam(25,math.radians(90)))
root = tk.Tk()
fig, ax = plt.subplots()
limit = math.sqrt(arm.beam1.length**2 + arm.beam2.length**2+arm.beam0.length**2)
# arduino = serial.Serial(port='COM6', baudrate=115200)

ax.set_ylim(0, limit+arm.beam0.length)
ax.set_xlim(-limit, limit)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

xin = tk.Entry(root)
xin.pack()
yin = tk.Entry(root)
yin.pack()
claw_pos = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="open claw", variable=claw_pos, onvalue=1, offvalue=0, command=arm.move_claw).pack()

update_button = tk.Button(root, text="Update", command=update)
update_button.pack()

root.mainloop()
