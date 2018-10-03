import json
import os

def ensureExists(file: str, isDir: bool = False):
    cur = "/"
    for part in file.split("/")[:-1]:
        if part == "":
            continue
        cur += part + "/"
        if not os.path.isdir(cur):
            os.mkdir(cur)

def getKey(key: str) -> dict:
    try:
        with open("/db" + key, "r") as f:
            return json.loads(f.read())
    except:
        return None

def setKey(key: str, value: dict):
    ensureExists("/db" + key)
    with open("/db" + key, "w") as f:
        f.write(json.dumps(value))

def listSubKeys(key: str) -> list:
    ensureExists("/db" + key + "/file.json")
    return os.listdir("/db" + key)
