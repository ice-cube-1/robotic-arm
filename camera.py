from picamera2 import Picamera2


class Camera:
    def __init__(self) -> None:
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.set_controls({"Contrast": 1.0})
        self.camera.start()

    def takePhoto(self) -> None: 
        self.camera.capture_file("static/image.jpg")
