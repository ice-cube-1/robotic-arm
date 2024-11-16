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
    arm = Arm(Beam(59.5+4,120,0), Beam(67.6+4,120,0),Beam(70.6+4,160,0),Beam(25,180,0,math.radians(90)))
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
            position = arm.setPosition(50.0,150.0)
            await websocket.send(json.dumps(position))
            sleep(2)
            arm.stepperPos = 0
            while arm.stepperPos < 100:
                arm.setStepper(arm.stepperPos)
                await websocket.send("stepperpos "+str(200-arm.stepperPos))
                distance=camera.distance()
                print(distance,arm.stepperPos)
                camera.takePhoto()
                await websocket.send("image")
                while 90 < distance < 200:
                    move = camera.getCentral()
                    camera.takePhoto()
                    await websocket.send("image")
                    if abs(move) <= 100:
                        barrels.append(Barrel(arm.stepperPos, distance))
                        [print(i.x,i.y, i.distance,i.angle) for i in barrels]
                        await websocket.send("barrel "+barrels[-1].getData())
                        arm.stepperPos+=25
                        break
                    if arm.stepperPos>100:
                        break
                    arm.stepperPos = arm.stepperPos-int(move/100)
                    arm.setStepper(arm.stepperPos)
                    await websocket.send("stepperpos "+str(200-arm.stepperPos))
                    sleep(2)
                    distance = camera.distance()
                    print(distance)
                arm.stepperPos+=10
                sleep(2)
        elif message[0] == "barrel":
            barrel = barrels[0]
            for i in range(len(barrels)): 
                if barrels[i].x == message[1] and barrels[i].y == message[2]:
                    position = arm.setPosition(50.0,150.0)
                    await websocket.send(json.dumps(position))
                    sleep(2)
                    arm.move_claw(45)
                    await websocket.send("claw 45")
                    sleep(2)
                    arm.setStepper(barrels[i].angle)
                    await websocket.send("stepperpos "+str(200-arm.stepperPos))
                    sleep(2)
                    position = arm.setPosition(barrels[i].distance, 30.0)
                    await websocket.send(json.dumps(position))
                    sleep(2)
                    arm.move_claw(0)
                    await websocket.send("claw 0")
                    barrels[i].gripped = True
                    await websocket.send("attached")
                    position = arm.setPosition(50.0,150.0)
                    await websocket.send(json.dumps(position))
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


    