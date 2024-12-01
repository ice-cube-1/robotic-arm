from movement import scan, pickup, drop, move, rotate

async def parse(arm, camera, websocket, barrels, code):
    old = ["scan(", "pickup(", "drop(", "rotate(", "move("]
    new = ["scan(arm, camera, websocket", 
           "pickup(arm, websocket, ", 
           "drop(arm, websocket, ",
           "rotate(arm, websocket, ",
           "move(arm, websocket, ",]
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
    localScope = {"arm": arm, "camera": camera, "websocket": websocket,
                "scan": scan, "pickup": pickup, "drop": drop, "move": move, "rotate": rotate}
    exec(code, localScope)
    await localScope["main"]()
    
