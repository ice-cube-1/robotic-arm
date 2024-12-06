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
    
    def returnPhoto(self):
        return self.camera.capture_array()

    def getContours(self):
        image = self.camera.capture_array()
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        # lower_red1 = np.array([0, 150, 80])
        # upper_red1 = np.array([10, 255, 255])
        # lower_red2 = np.array([170, 150, 80])
        # upper_red2 = np.array([180, 255, 255])
        # mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        # mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        # red_object = cv2.bitwise_and(image, image, mask=mask1 | mask2) # type: ignore
        # contours, _ = cv2.findContours(mask1 | mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # type: ignore
        lower_yellow = np.array([10, 150, 80])
        upper_yellow = np.array([55, 255, 255])
        mask1 = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellowObject = cv2.bitwise_and(image, image, mask=mask1)
        contours, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return sorted(contours, key=cv2.contourArea, reverse=True), "yellow"


    def distance(self) -> float:
        contours,color = self.getContours()
        if contours:
            w = cv2.boundingRect(contours[0])[2]
            distance = 46600/w
            return distance-20, color
        else:
            return 0, "red"
    
    def getCentral(self) -> int:
        contours, color = self.getContours()
        if contours:
            rect = cv2.boundingRect(contours[0])
            difference = (3280/2)-(rect[0]+(rect[2]/2))
            return int(difference)
        return 20000