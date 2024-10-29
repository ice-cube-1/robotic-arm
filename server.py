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
            if message[1] == "45":
                for i in range(len(barrels)):
                    if barrels[i].gripped==True:
                        barrels[i] = Barrel(arm.stepperPos, arm.beam3.endy)
                        barrels[i].gripped = False
                        await websocket.send("dropped "+barrels[i].getData())
            arm.move_claw(float(message[1]))
        elif message[0] == "photo":
            print("photo requested")
            camera.takePhoto()
            await websocket.send("image")
        elif message[0] == "scan":
            await websocket.send(json.dumps(arm.setPosition(50,150)))
            arm.stepperPos = -25
            while arm.stepperPos < 200:
                arm.setStepper(arm.stepperPos+25)
                if 90 < camera.distance() < 180:
                    while True:
                        move = camera.getCentral()
                        await websocket.send("image")
                        if abs(move) <= 100: break
                        arm.setStepper(int(move/100))
                        await websocket.send("stepperpos "+str(arm.stepperPos))
                        sleep(2)
                    barrels.append(Barrel(arm.stepperPos, camera.distance()))
                    await websocket.send("barrel "+barrels[-1].getData())
        elif message[0] == "barrel":
            barrel = barrels[0]
            for i in range(len(barrels)): 
                if barrels[i].x == message[1] and barrels[i].y == message[2]:
                    await websocket.send(json.dumps(arm.setPosition(50,150)))
                    sleep(2)
                    arm.move_claw(45)
                    await websocket.send("claw 45")
                    sleep(2)
                    arm.setStepper(barrels[i].angle)
                    await websocket.send("stepperpos "+str(arm.stepperPos))
                    sleep(2)
                    await websocket.send(json.dumps(arm.setPosition(barrels[i].distance, 0)))
                    sleep(2)
                    arm.move_claw(0)
                    await websocket.send("claw 0")
                    barrels[i].gripped = True
                    await websocket.send("attached")
                    await websocket.send(json.dumps(arm.setPosition(50,150)))
        else:
            positions = arm.setPosition(float(message[0]),float(message[1]))
            if positions != []:
                await websocket.send(json.dumps(positions))
            await websocket.send("stepperpos "+json.dumps(message[2]))


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


    