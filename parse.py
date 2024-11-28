from movement import scan, pickup, drop, move, rotate

def parse(code, arm, camera, websocket, barrels):
    code = "".join(open("sampleCode.txt").readlines())
    old = ["scan(", "pickup(", "drop(", "rotate(", "move("]
    new = ["scan(arm, camera, websocket, barrels, ", 
           "pickup(arm, websocket, barrels, ", 
           "drop(arm, websocket, barrels, ",
           "rotate(arm, websocket, ",
           "move(arm, websocket, "]
    i=0
    while i < len(code):
        addParams(code,)
        if len(code)-i > len("scan()") and code[i:i+len("scan()")] == "scan()":
            code = code[:i]+"scan(arm, camera, websocket, barrels)"+code[i+len("scan()"):]
        if len(code)-i > len("pickup(") and code[i:i+len("pickup(")] == "pickup(":
            code = code[:i]+"pickup(arm, websocket, barrels"+code[i+len("pickup("):]
        if len(code)-i > len("drop(") and code[i:i+len("drop(")] == "drop(":
            code = code[:i]+"drop(arm, websocket, barrels"+code[i+len("drop("):]
        i+=1
    print(code)
    exec(code)

def addParams(code, old: list[str], new: list[str], i):
    for j in range(len(old)):
        if len(code)-i > len(old[j]) and code[i:i+len(old[j])] == old[j]:
            code = code[:i]+new[j]+code[i+len(old[j]):]
