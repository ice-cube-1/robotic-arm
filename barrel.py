import math

class Barrel:
    def __init__(self, angle: int, distance: float, color: str) -> None:
        self.x: int = round(distance*math.cos(math.radians(angle*1.8)))
        self.y: int = round(-distance*math.sin(math.radians(angle*1.8)))
        self.angle = angle
        self.distance = distance
        self.gripped: bool = False
        self.color: str = color
        
    def getData(self) -> str:
        return str(self.x)+" "+str(self.y)+" "+self.color
