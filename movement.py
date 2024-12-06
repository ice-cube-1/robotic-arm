from time import sleep
import json
from barrel import Barrel
import math
from arm_info import Arm
from camera import Camera
import websockets

async def scan(arm: Arm, camera: Camera, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel] = []):
        position = arm.setPosition(50.0,150.0)
        await websocket.send(json.dumps(position))
        sleep(2)
        end = arm.stepperPos+100 # CHANGE TO 200
        while arm.stepperPos < end:
            arm.setStepper(arm.stepperPos)
            await websocket.send("stepperpos "+str(200-arm.stepperPos))
            sleep(2)
            distance,color =camera.distance()
            print(distance,arm.stepperPos)
            while 90 < distance < 240:
                move = camera.getCentral()
                print(distance,move)
                if abs(move) <= 100:
                    barrels.append(Barrel(arm.stepperPos, distance, color))
                    [print(i.x,i.y, i.distance,i.angle) for i in barrels]
                    await websocket.send("barrel "+barrels[-1].getData())
                    arm.stepperPos+=25
                    break
                if arm.stepperPos>end:
                    break
                arm.stepperPos = arm.stepperPos-int(move/100)
                arm.setStepper(arm.stepperPos)
                await websocket.send("stepperpos "+str(200-arm.stepperPos))
                sleep(2)
                distance, color = camera.distance()
                print(distance)
            arm.stepperPos+=10
            sleep(2)
        return barrels
        
async def pickup(arm: Arm, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel], i: int):
    position = arm.setPosition(50.0,150.0)
    await websocket.send(json.dumps(position))
    sleep(2)
    arm.move_claw(45)
    await websocket.send("claw "+str(math.pi/2))
    sleep(2)
    arm.setStepper(barrels[i].angle)
    await websocket.send("stepperpos "+str(200-arm.stepperPos))
    sleep(2)
    position = arm.setPosition(barrels[i].distance, 70.0)
    await websocket.send(json.dumps(position))
    sleep(2)
    arm.move_claw(0)
    await websocket.send("claw "+str(math.pi/4))
    barrels[i].gripped = True
    await websocket.send("attached")
    position = arm.setPosition(50.0,150.0)
    await websocket.send(json.dumps(position))

async def drop(arm: Arm, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel]):
    for i in range(len(barrels)):
        if barrels[i].gripped==True:
            barrels[i] = Barrel(arm.stepperPos, arm.beam3.endy)
            barrels[i].gripped = False
            await websocket.send("dropped "+barrels[i].getData())
    arm.move_claw(45)
    return barrels

async def move(arm: Arm, websocket: websockets.WebSocketServerProtocol, x, y):
    positions = arm.setPosition(x,y)
    await websocket.send(json.dumps(positions))

async def rotate(arm: Arm, websocket: websockets.WebSocketServerProtocol, stepperpos: int):
    arm.setStepper(stepperpos)
    await websocket.send("stepperpos "+str(200-arm.stepperPos))
    sleep(2)