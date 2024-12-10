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
        lower_red1 = np.array([0, 150, 80])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 150, 80])
        upper_red2 = np.array([180, 255, 255])
        redMask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        redMask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        redObject = cv2.bitwise_and(image, image, mask=redMask1 | redMask2) # type: ignore
        redContours, _ = cv2.findContours(redMask1 | redMask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # type: ignore
        red = sorted(redContours, key=cv2.contourArea, reverse=True)

        lower_yellow = np.array([10, 150, 80])
        upper_yellow = np.array([55, 255, 255])
        yellowMask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellowObject = cv2.bitwise_and(image, image, mask=yellowMask)
        yellowContours, _ = cv2.findContours(yellowMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow = sorted(yellowContours, key=cv2.contourArea, reverse=True)
        
        lower_blue = np.array([90, 150, 80])
        upper_blue = np.array([130, 255, 255])
        blueMask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        blueObject = cv2.bitwise_and(image, image, mask=blueMask)
        blueContours, _ = cv2.findContours(blueMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue = sorted(blueContours, key=cv2.contourArea, reverse=True)
        if blue:
            if red:
                if yellow:       
                    if cv2.contourArea(blue[0]) == max(cv2.contourArea(blue[0]), cv2.contourArea(red[0]), cv2.contourArea(yellow[0])):
                        return blue, "blue"
                    if cv2.contourArea(red[0]) > cv2.contourArea(yellow[0]):
                        return red, "red"
                    else:
                        return yellow, "yellow"
                else:
                    if cv2.contourArea(red[0]) > cv2.contourArea(blue[0]):
                        return red, "red"
                    else:
                        return blue, "blue"
            else:
                if yellow:
                    if cv2.contourArea(yellow[0]) > cv2.contourArea(blue[0]):
                        return yellow, "yellow"
                    else:
                        return blue, "blue"
                else:
                    return blue, "blue"
        else:
            if red:
                if yellow:
                    if cv2.contourArea(red[0]) > cv2.contourArea(yellow[0]):
                        return red, "red"
                    else:
                        return yellow, "yellow"
                else:
                    return red, "red"
            else:
                if yellow:
                    return yellow, "yellow"
                else: return -1



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