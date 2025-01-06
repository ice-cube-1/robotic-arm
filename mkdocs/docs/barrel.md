## Barrel

Barrels should not be manually created, but retrieving their properties is often useful.

## Methods

    self.angle: int
    self.distance: float

The angle (in steps, so 200 per full rotation) of the stepper when the barrel is directly in the center of its vision, and the distance the barrel is away from the pivot.

    self.x: int
    self.y: int

Polar to cartesian conversions of angle and distance

    self.gripped: bool = False

Whether the barrel is currently held by the claw, in which case the position information is incorrect.

    self.color: str

The colour of the barrel (red, yellow or blue)

## Return data

    getData(self) -> str

returns the x, y and colour in a space-delimited string (used for websocket transmission)