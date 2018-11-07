from code.util.db import getKey, setKey
from uuid import uuid4

users = {}
userNames = {}

class User:
    def __init__(self, id: str, name: str, password: str, type: str):
        self.id = id
        self.name = name
        self.password = password
        self.type = type
    
    def get(id: str):
        if id in users:
            return users[id]
        return None
    
    def getByName(name: str):
        if name in userNames:
            return userNames[name]
        return None
    
    def save(self):
        if self.id == None:
            self.id = str(uuid4())
            users[self.id] = self
            userNames[self.name] = self
        usrs = [users[id].toJSON() for id in users]
        setKey("/users.json", usrs)
    
    def toJSON():
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "type": self.type
        }

usrs = getKey("/users.json") or []
for usr in usrs:
    user = User(usr["id"], usr["name"], usr["password"], usr["type"])
    users[usr["id"]] = user
    userNames[usr["name"]] = user
