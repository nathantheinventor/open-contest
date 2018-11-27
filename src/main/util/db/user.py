from code.util.db import getKey, setKey
from uuid import uuid4
import logging

users = {}
userNames = {}

class User:
    def __init__(self, username: str, password: str, type: str, id: str = None):
        self.id = id
        if username in userNames:
            self.id = userNames[username].id
        self.username = username
        self.password = password
        self.type = type
    
    def get(id: str):
        if id in users:
            return users[id]
        return None
    
    def getByName(username: str):
        if username in userNames:
            return userNames[username]
        return None
    
    def save(self):
        logging.info(f"saving {self.username}")
        if self.id == None:
            self.id = str(uuid4())
            users[self.id] = self
            userNames[self.username] = self
        usrs = [users[id].toJSON() for id in users]
        setKey("/users.json", usrs)
    
    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "type": self.type
        }
    
    def allJSON():
        return [users[id].toJSON() for id in users]
    
    def delete(self):
        del users[self.id]
        del userNames[self.username]
        self.save()
    
    def isAdmin(self) -> bool:
        return self.type == "admin"

usrs = getKey("/users.json") or []
for usr in usrs:
    user = User(usr["username"], usr["password"], usr["type"], usr["id"])
    users[usr["id"]] = user
    userNames[usr["username"]] = user
