import asyncio
import websockets
from aiohttp import web
from arm_info import Arm, Beam
import math
import json
from camera import Camera
from time import sleep
from barrel import Barrel

async def echo(websocket):
    arm = Arm(Beam(59.5+4), Beam(67.6+4),Beam(70.6+4),Beam(25,math.radians(90)))
    camera = Camera()
    barrels: list[Barrel] = []
    async for message in websocket:
        print(message)
        message = message.split()
        if message[0] == "claw":
            print(message[1])
            arm.move_claw(float(message[1]))
        elif message[0] == "photo":
            print("photo requested")
            camera.takePhoto()
            await websocket.send("image")
        elif message[0] == "distance":
            await websocket.send("distance: "+ str(camera.distance()))
        elif message[0] == "scan":
            arm.setPosition(50,150)
            arm.stepperPos = -25
            while arm.stepperPos < 200:
                arm.setStepper(arm.stepperPos+25)
                if 90 < camera.distance() < 180:
                    while True:
                        move = camera.getCentral()
                        if abs(move) <= 100: break
                        arm.setStepper(int(move/100))
                        sleep(2)
                    barrels.append(Barrel(arm.stepperPos, camera.distance()))
                    await websocket.send("barrel "+barrels[-1].getData())
                
        else:
            positions = arm.setPosition(float(message[0]),float(message[1]))
            if positions != []:
                await websocket.send(json.dumps(positions))


async def handle_html(_):
        return web.FileResponse('./index.html')

async def start_servers():
    webocket_server = websockets.serve(echo, "192.168.137.81", 8765)
    app = web.Application()
    app.router.add_get('/', handle_html)
    app.router.add_static('/static/', path='./static', name='static')
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "192.168.137.81", 8080)
    await asyncio.gather(webocket_server, site.start())

asyncio.get_event_loop().run_until_complete(start_servers())
asyncio.get_event_loop().run_forever()


    