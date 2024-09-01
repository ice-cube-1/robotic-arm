import math
import matplotlib.pyplot as plt

len1 = 20
len2 = 10

def law_of_cosines(a, b, c):
    """Calculate the angle C using the law of cosines."""
    return math.acos((a * a + b * b - c * c) / (2 * a * b))

def distance(x, y):
    """Calculate the distance from (0,0) to (x,y)."""
    return math.sqrt(x * x + y * y)

def angles(x, y):
    """Calculate the angles for given x and y."""
    dist = distance(x, y)
    D1 = math.atan2(y, x)
    D2 = law_of_cosines(dist, len1, len2)
    A1 = D1 + D2
    A2 = law_of_cosines(len1, len2, dist)
    return A1, A2

def arm_positions(x, y):
    """Calculate the positions of each segment of the arm."""
    try:
        A1, A2 = angles(x, y)
        x1_end = len1 * math.cos(A1)
        y1_end = len1 * math.sin(A1)
        x2_end = x1_end+len2 * -math.cos(A1 + A2)
        y2_end = y1_end+len2 * -math.sin(A1 + A2) 
        return (0, 0), (x1_end, y1_end), (x2_end, y2_end)
    except:
         print(x,y)
         return (0,0), (0,0)

def deg(rad):
    """Convert radians into degrees."""
    return rad * 180 / math.pi

data = []

for i in range(0, 20,2):
    for j in range(-20, 20,2):
            x, y = zip(*arm_positions(i,j))
            plt.plot(x,y)

plt.show()