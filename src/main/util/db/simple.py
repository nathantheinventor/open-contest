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
            s = f.read()
            if s[0] in ("[", "{"):
                return json.loads(s)
            return s
    except Exception as e:
        print(e)
        return None

def setKey(key: str, value):
    ensureExists("/db" + key)
    with open("/db" + key, "w") as f:
        if isinstance(value, dict):
            f.write(json.dumps(value))
        else:
            f.write(value)

def listSubKeys(key: str) -> list:
    ensureExists("/db" + key + "/file.json")
    return [x for x in os.listdir("/db" + key) if not x.startswith(".")]

def deleteKey(key: str):
    os.unlink("/db" + key)
