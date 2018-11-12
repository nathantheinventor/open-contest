from code.util.db import getKey, setKey
from uuid import uuid4
import logging

users = {}
userNames = {}

class User:
    def __init__(self, id: str, username: str, password: str, type: str):
        self.id = id
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

usrs = getKey("/users.json") or []
for usr in usrs:
    user = User(usr["id"], usr["username"], usr["password"], usr["type"])
    users[usr["id"]] = user
    userNames[usr["username"]] = user
