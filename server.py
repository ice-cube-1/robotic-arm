import asyncio
import websockets
from aiohttp import web
from arm_info import Arm, Beam
import math
import json
from camera import Camera
from time import sleep
from barrel import Barrel
from parse import parse
from movement import scan, pickup, drop

async def echo(websocket: websockets.WebSocketServerProtocol):
    arm = Arm(Beam(59.5+4,120,0), Beam(67.6+4,120,0),Beam(70.6+4,160,0),Beam(25,180,0,math.radians(90)))
    camera = Camera()
    barrels: list[Barrel] = []
    async for message in websocket:
        if message[:len("code: ")] == "code: ":
            await parse(arm, camera, websocket, barrels, message[len("code: "):])
            break
        print(message)
        message = message.split()
        if message[0] == "claw":
            if message[1] == "45":
                drop()
            arm.move_claw(float(message[1]))
        elif message[0] == "photo":
            print("photo requested")
            camera.takePhoto()
            await websocket.send("image")
        elif message[0] == "scan":
            barrels = await scan(arm, camera, websocket, barrels)
        elif message[0] == "barrel":
            for i in range(len(barrels)): 
                if barrels[i].x == int(message[1]) and barrels[i].y == int(message[2]):
                    print("going to barrel")
                    pickup(arm, camera, websocket, barrels, i)
        else:
            positions = arm.setPosition(float(message[0]),float(message[1]))
            sleep(2)
            arm.setStepper(int(message[2]))
            if positions != []: await websocket.send(json.dumps(positions))
            else: await websocket.send("error")
            await websocket.send("stepperpos "+str(200-arm.stepperPos))


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


    