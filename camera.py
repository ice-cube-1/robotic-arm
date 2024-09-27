from picamera2 import Picamera2


class Camera:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.start()

    def takePhoto(self): 
        return self.camera.capture_array()