# Camera

An instance of the camera called camera has already been created. Do not attempt to re-initialise the class.

## Take photo

    camera.takePhoto(self) -> None

Takes a picture and saves it to static/image.jpg. This will not update the webserver until you send a command via websocket notifying the client of the update.

    camera.takePhoto()
    await websocket.send("image")

This cannot be done repeatedly with very little delay as it causes read/write conflicts on the file.

## Distance

    camera.distance(self) -> tuple(float, str)

This returns the distance of the nearest red, yellow or blue object and its color (this is likely a barrel if the value is reasonable, and empty space if not)

## Centre

    camera.getCentral(self) -> int

Returns the number of pixels the center of the detected object is from the center (less than 100 generally means it is centered)