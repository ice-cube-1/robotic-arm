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
        maxContours = dict()
        image = self.camera.capture_array()
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower_red1 = np.array([0, 150, 80])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 150, 80])
        upper_red2 = np.array([180, 255, 255])
        redMask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        redMask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        redContours, _ = cv2.findContours(redMask1 | redMask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # type: ignore
        if len(redContours)!=0:
            red = sorted(redContours, key=cv2.contourArea, reverse=True)
            maxContours[red[0]] = "red"

        lower_yellow = np.array([10, 150, 80])
        upper_yellow = np.array([55, 255, 255])
        yellowMask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellowContours, _ = cv2.findContours(yellowMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(yellowContours)!=0:
            yellow = sorted(yellowContours, key=cv2.contourArea, reverse=True)
            maxContours[yellow[0]] = "yellow"

        lower_blue = np.array([90, 150, 80])
        upper_blue = np.array([130, 255, 255])
        blueMask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        blueContours, _ = cv2.findContours(blueMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(blueContours)!=0:
            blue = sorted(blueContours, key=cv2.contourArea, reverse=True)
            maxContours[blue[0]] = "blue"

        if len(maxContours)==0:
            return -1, "red"
        
        largest = max(maxContours.keys(), key=cv2.contourArea)
        return largest, maxContours[largest]


    def distance(self) -> tuple[float, str]:
        contours,color = self.getContours()
        if contours != -1:
            w = cv2.boundingRect(contours)[2]
            distance = 46600/w
            return distance-20, color
        else:
            return 0, "red"
    
    def getCentral(self) -> int:
        contours, _ = self.getContours()
        if contours != -1:
            rect = cv2.boundingRect(contours)
            difference = (3280/2)-(rect[0]+(rect[2]/2))
            return int(difference)
        return 20000