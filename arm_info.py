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
    def __init__(self, length: float, tmin: float, tmax: float):
        self.length = length
        self.tmin = math.radians(tmin)
        self.tmax = math.radians(tmax)
        self.t: float = 0
        self.endx: float = 0
        self.endy: float = 0
        


class Arm:
    def __init__(self, height: float, beam1: Beam, beam2: Beam, maxWidth: float) -> None:
        self.beam1 = beam1
        self.beam2 = beam2
        self.height = height
        self.maxWidth = maxWidth

    def setPosition(self, x: float, y: float) -> bool:
        try:
            y = y-self.height
            dist: float = distance(x, y)
            D1 = math.atan2(y, x)
            D2 = law_of_cosines(dist, self.beam1.length, self.beam2.length)
            self.beam1.t = D1 + D2
            self.beam2.t = law_of_cosines(self.beam1.length, self.beam2.length, dist)
            self.beam1.endx = self.beam1.length * math.cos(self.beam1.t)
            self.beam1.endy = self.beam1.length * math.sin(self.beam1.t)+self.height
            self.beam2.endx = self.beam1.endx - self.beam2.length * math.cos(self.beam1.t + self.beam2.t)
            self.beam2.endy = self.beam1.endy - self.beam2.length * math.sin(self.beam1.t + self.beam2.t)
            return True
        except:
            return False
    
    def plotInfo(self) -> list[list[float]]:
        return [[0,0, self.beam1.endx, self.beam2.endx], [0, self.height, self.beam1.endy, self.beam2.endy]]
    
    def sendToArduino(self) -> None:
        angle = 135-int(math.degrees(self.beam1.t))
        arduino.write(bytes("1" + str(angle) + "\n", 'utf-8'))
        print(angle)        
        sleep(1)
        angle = 180-int(math.degrees(self.beam2.t)-30)
        arduino.write(bytes("2" + str(angle) + "\n", 'utf-8'))
        print(angle)

def update():
    if arm.setPosition(float(xin.get()), float(yin.get())):
        data = arm.plotInfo()
        arm.sendToArduino()
        ax.clear()
        ax.plot(data[0], data[1])
        ax.set_xlim(-limit, limit)
        ax.set_ylim(0, limit+arm.height)
        canvas.draw()

arm = Arm(80.25, Beam(101.25,math.radians(-45),math.radians(115)),Beam(36,math.radians(20),math.radians(200)),25)
root = tk.Tk()
fig, ax = plt.subplots()
limit = math.sqrt(arm.beam1.length**2 + arm.beam2.length**2+arm.height**2)
arduino = serial.Serial(port='COM6',   baudrate=115200)

ax.set_ylim(0, limit+arm.height)
ax.set_xlim(-limit, limit)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

xin = tk.Entry(root)
xin.pack()
yin = tk.Entry(root)
yin.pack()

update_button = tk.Button(root, text="Update", command=update)
update_button.pack()

root.mainloop()
