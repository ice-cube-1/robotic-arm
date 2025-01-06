import movement
from arm_info import Arm
from camera import Camera
from barrel import Barrel
import websockets

async def parse(arm: Arm, camera: Camera, websocket: websockets.WebSocketServerProtocol, barrels: list[Barrel], code: str) -> list[Barrel]:
    print(code)
    scan = lambda *args: movement.scan(arm, camera, websocket, *args)
    pickup = lambda *args: movement.pickup(arm, camera, websocket, *args)
    drop = lambda *args: movement.drop(arm, websocket, *args)
    rotate = lambda *args: movement.rotate(arm, websocket, *args)
    move = lambda *args: movement.rotate(arm, websocket, *args)
    async def output(x):
        print("outputting",x)
        await websocket.send("output "+x)
    await output("clear")
    code = (
        "try:\n" +
        ''.join(f'    {line}\n' for line in code.split('\n')) +
        "except Exception as e:\n"
        "    await output(f'Error: {str(e)}')"
    )
    exec(
        f'async def __ex(): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
        , locals()
    )
    await locals()['__ex']()
    await output("done :)")
    print("done")
    return barrels

