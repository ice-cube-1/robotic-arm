from time import sleep
import json
from barrel import Barrel
import math
from arm_info import Arm
from camera import Camera
import websockets

async def scan(arm: Arm, camera: Camera, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel] = []) -> list[Barrel]:
        barrels = [i for i in barrels if i.gripped]
        position = arm.setPosition(100.0,250.0)
        await websocket.send(json.dumps(position))
        sleep(2)
        end = arm.stepperPos+200
        while arm.stepperPos < end:
            arm.setStepper(arm.stepperPos)
            await websocket.send("stepperpos "+str(200-arm.stepperPos))
            sleep(2)
            distance,color =camera.distance()
            print(distance,color)
            while 90 < distance < 400 and (5 < arm.stepperPos%200 < 195):
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
        
async def pickup(arm: Arm, camera, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel], i: int) -> list[Barrel]:
    if not (190 <= barrels[i].distance <= 230):
         await websocket.send("barrelerror")
         return
    success = False
    while not success:
        position = arm.setPosition(100.0,250.0)
        await websocket.send(json.dumps(position))
        sleep(2)
        arm.move_claw(45)
        await websocket.send("claw "+str(math.pi/2))
        sleep(2)
        arm.setStepper(barrels[i].angle)
        move = camera.getCentral()
        sleep(2)
        while abs(move) > 100:
            arm.stepperPos = arm.stepperPos-int(move/100)
            arm.setStepper(arm.stepperPos)
            await websocket.send("stepperpos "+str(200-arm.stepperPos))
            move = camera.getCentral()
            sleep(2)
        sleep(2)
        arm.setStepper(arm.stepperPos)
        await websocket.send("stepperpos "+str(200-arm.stepperPos))
        sleep(2)
        position = arm.setPosition(170.0, 20.0)
        await websocket.send(json.dumps(position))
        sleep(2)
        position = arm.setPosition(barrels[i].distance, 50.0)
        print("important stuff", position, barrels[i].distance)
        await websocket.send(json.dumps(position))
        sleep(2)
        arm.move_claw(0)
        await websocket.send("claw "+str(math.pi/4))
        sleep(2)
        position = arm.setPosition(150.0,200.0)
        await websocket.send(json.dumps(position))
        print("has picked up?", camera.getCentral(), camera.distance()[0], barrels[i].distance)
        if not (camera.getCentral()<100 and abs(camera.distance()[0]-barrels[i].distance)<50):
            success= True
            barrels[i].gripped = True
            await websocket.send("attached")
            return barrels
        print("retrying")


async def drop(arm: Arm, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel]) -> list[Barrel]:
    for i in range(len(barrels)):
        if barrels[i].gripped==True:
            barrels[i] = Barrel(arm.stepperPos, arm.beam3.endy, barrels[i].color)
            barrels[i].gripped = False
            await websocket.send("dropped "+barrels[i].getData())
    arm.move_claw(45)
    return barrels

async def move(arm: Arm, websocket: websockets.WebSocketServerProtocol, x, y) -> None:
    positions = arm.setPosition(x,y)
    await websocket.send(json.dumps(positions))
    sleep(2)

async def rotate(arm: Arm, websocket: websockets.WebSocketServerProtocol, stepperpos: int) -> None:
    arm.setStepper(stepperpos)
    await websocket.send("stepperpos "+str(200-arm.stepperPos))
    sleep(2)
