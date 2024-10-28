import math

class Barrel:
    def __init__(self, angle, distance) -> None:
        self.x: float = distance*math.sin(math.radians(angle*1.8))
        self.y: float = distance*math.cos(math.radians(angle*1.8))

    def getData(self) -> str:
        return str(self.x)+" "+str(self.y)