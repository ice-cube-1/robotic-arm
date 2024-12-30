import movement

async def parse(arm, camera, websocket, barrels, code):
    print(code)
    scan = lambda *args: movement.scan(arm, camera, websocket, *args)
    pickup = lambda *args: movement.pickup(arm, camera, websocket, *args)
    drop = lambda *args: movement.drop(arm, websocket, *args)
    rotate = lambda *args: movement.rotate(arm, websocket, *args)
    move = lambda *args: movement.rotate(arm, websocket, *args)
    exec(
        f'async def __ex(): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
        , locals()
    )
    await locals()['__ex']()
    print(barrels)
    print("done")
    return barrels
