import asyncio
import websockets
from arm_info import Arm, Beam
import math
import json


async def echo(websocket):
    arm = Arm(Beam(59.5), Beam(67.6),Beam(67.6),Beam(25,math.radians(90)))
    async for message in websocket:
        message = message.split()
        positions = arm.setPosition(float(message[0]),float(message[1]))
        print(json.dumps(positions))
        if positions != []:
            await websocket.send(json.dumps(positions))

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


    