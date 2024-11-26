from movement import scan

def parse():#arm, camera, websocket, barrels):
    code = "".join(open("sampleCode.txt").readlines())
    i=0
    while i < len(code):
        if len(code)-i > len("scan()") and code[i:i+len("scan()")] == "scan()":
            code = code[:i]+"scan(arm, camera, websocket, barrels)"+code[i+len("scan()"):]
        if len(code)-i > len("pickup(") and code[i:i+len("pickup(")] == "pickup(":
            code = code[:i]+"pickup(arm, websocket, barrels"+code[i+len("pickup("):]
        if len(code)-i > len("drop(") and code[i:i+len("drop(")] == "drop(":
            code = code[:i]+"drop(arm, websocket, barrels"+code[i+len("drop("):]
        i+=1
    print(code)
    exec(code)
parse()