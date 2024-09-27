from picamera2 import Picamera2

def setup():
    picam2 = Picamera2()
    picam2.start()
    return picam2

def takePhoto(camera): 
    return camera.capture_array()