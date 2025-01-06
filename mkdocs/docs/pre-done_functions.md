# Pre-done functions

Some extra points to note about using these:

* Any function defined must be asynchronous as the code is all run within an async function. Likewise, any of the below functions must be called with await.

        async def x():
            await output("hello")
        await x()

* These functions have extra parameters that are automatically passed in from your code. These are the arm, the websocket and the camera (scan and pickup only).

## Scan
This scans a full 360 degrees ands adds any barrels it detects to the render.

    async def scan(barrels: list[Barrel] = []) -> list[Barrel]

This works as follows:

1. The arm moves up, giving it an unobstructed view of the ground
2. It continuously rotates until the calculated distance to the nearest barrel is within 90 < distance < 300 (it believes a barrel to be somewhere in frame).
3. It attempts to center on the barrel
4. The barrel's colour and position is then added to the list of barrels, and sent back to the website via websocket
5. This repeats until it has reached the start point, when it returns a list of all barrels detected

Any barrels passed in will be removed unless they are currently gripped.

## Pickup
From the list of barrels passed in, it picks up the one at index i.

    async def pickup(barrels: list[Barrel], i: int) -> list[Barrel]

This moves the arm out of the way before rotating, then recenters on the barrel (in case accidental movement has offset the position slightly) and reaches down to pick it up. It then moves back up, and will repeat the whole proess if the barrel is still there.

## Drop
Drops the current barrel, presuming it falls directly down and lands upright.

    async def drop(barrels: list[Barrel]) -> list[Barrel]

This is just a wrapper for the open claw function, but deals with sending data via websocket as well. This requires the arm to currently be very close to the ground to work successfully, as the arm does not move down automatically.

## Move
Moves the arm to the requested x (horizontal distance from pivot, mm) and y (vertical distance from pivot), without any rotation.

    async def move(x: float, y: float) -> None

## Rotate
Rotates the entire arm, taking into account that it cannot continuously rotate in one direction. A full 360 degree rotation is divided into 200 steps.

    async def rotate(steps: int) -> None

## Output
Print statements do not work in this UI, so this is the asynchronous equivalent. These show up to the right of the code input, acting as a basic console.

    async def output(x: str) -> None
