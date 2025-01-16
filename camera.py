from picamera2 import Picamera2
import cv2
import numpy as np


class Camera:
    def __init__(self) -> None:
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.start()

    def takePhoto(self) -> None: 
        self.camera.capture_file("static/image.jpg")
    
    def returnPhoto(self) -> np.ndarray:
        return self.camera.capture_array()

    def getContours(self) -> tuple[np.ndarray | int, str]:
        image = self.camera.capture_array()
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        maxContourArea = 0
        contour = (-1,"red")
        colors = {
            "red": [(np.array([0, 150, 80]), np.array([10, 255, 255])),
                    (np.array([170, 150, 80]), np.array([180, 255, 255]))],
            "yellow": [(np.array([10, 150, 80]), np.array([55, 255, 255]))],
            "green": [(np.array([70, 150, 80]), np.array([100, 255, 255]))],
            "blue": [(np.array([100, 150, 80]), np.array([130, 255, 255]))]
        }

        for color in colors:
            mask = cv2.inRange(hsv_image, colors[color][0][0], colors[color][0][1])
            if len(colors[color]) == 2:
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv_image, colors[color][1][0], colors[color][1][1]))
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
                contours = sorted(contours, key=cv2.contourArea, reverse=True)
                if cv2.contourArea(contours[0]) > maxContourArea:
                    maxContourArea = cv2.contourArea(contours[0])
                    contour = (contours[0],color)
        return contour

    def distance(self) -> tuple[float, str]:
        contours,color = self.getContours()
        if type(contours) != int:
            w = cv2.boundingRect(contours)[2]
            distance = 46600/w
            return distance-15, color
        else:
            return 0, "red"
    
    def getCentral(self) -> int:
        contours, _ = self.getContours()
        if type(contours) != int:
            rect = cv2.boundingRect(contours)
            difference = (3280/2)-(rect[0]+(rect[2]/2))
            return int(difference)
        return 20000
