import json

def getKey(key: str) -> dict:
    try:
        with open("/db" + key, "r") as f:
            return json.loads(f.read())
    except:
        return None

def setKey(key: str, value: dict):
    with open("/db" + key, "w") as f:
        f.write(json.dumps(value))
