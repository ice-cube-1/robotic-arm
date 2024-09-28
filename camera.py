from picamera2 import Picamera2
import cv2
import numpy as np


class Camera:
    def __init__(self) -> None:
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.set_controls({"Contrast": 1.0})
        self.camera.start()

    def takePhoto(self) -> None: 
        self.camera.capture_file("static/image.jpg")
    
    def returnPhoto(self):
        return self.camera.capture_array()

    def distance(self) -> float | None:
        image = self.camera.capture_array()
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])
        mask = cv2.inRange(hsv_image, lower_green, upper_green)
        green_object = cv2.bitwise_and(image, image, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        if contours:
            w = cv2.boundingRect(contours[0])[2]
            distance = (56 * 631.6970304811) / w**0.7938
            return distance
        else:
            return none