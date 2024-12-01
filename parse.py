from movement import scan, pickup, drop, move, rotate

async def parse(arm, camera, websocket, barrels, code):
    old = ["scan(", "pickup(", "drop(", "rotate(", "move(", "run("]
    new = ["await scan(arm, camera, websocket, []", 
           "pickup(arm, websocket, barrels, ", 
           "drop(arm, websocket, barrels, ",
           "rotate(arm, websocket, ",
           "move(arm, websocket, ",
           "asyncio.run("]
    i=0
    while i < len(code):
        for j in range(len(old)):
            if len(code)-i > len(old[j]):
                if code[i:i+len(old[j])] == old[j]:
                    print("replacing")
                    code = code[:i]+new[j]+code[i+len(old[j]):]
                    i+=8
        i+=1
    print(code)
    print(barrels)
    exec(code, {"arm": arm, "camera": camera, "websocket": websocket, 
                "scan": scan, "pickup": pickup, "drop": drop, "move": move, "rotate": rotate})
