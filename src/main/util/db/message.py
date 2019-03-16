from code.util.db import getKey, setKey, listSubKeys, deleteKey, User
from uuid import uuid4
from readerwriterlock import rwlock

lock = rwlock.RWLockWrite()

messages = {}

class Message:
    saveCallbacks = []
    def __init__(self, id=None):
        if id != None:
            details = getKey(f"/messages/{id}/message.json")
            self.id          = details["id"]
            self.fromUser    = User.get(details["from"])
            self.toUser      = User.get(details["to"])
            self.isGeneral   = bool(details["general"])
            self.isAdmin     = bool(details["admin"])   # Message sent to admin
            self.message     = details["message"]
            self.timestamp   = float(details["timestamp"])
            self.replyTo     = details.get("replyTo")
        else:
            self.id          = None
            self.fromUser    = None
            self.toUser      = None
            self.isGeneral   = False
            self.isAdmin     = False
            self.message     = ""
            self.timestamp   = 0
            self.replyTo     = None

    def get(id: str):
        with lock.gen_rlock():
            if id in messages:
                return messages[id]
            return None
    
    def toJSONSimple(self):
        return {
            "id":        self.id,
            "from":      self.fromUser.id,
            "to":        self.toUser.id if self.toUser else None,
            "general":   self.isGeneral,
            "admin":     self.isAdmin,
            "message":   self.message,
            "timestamp": self.timestamp,
            "replyTo":   self.replyTo
        }

    def save(self):
        with lock.gen_wlock():
            if self.id == None:
                self.id = str(uuid4())
                messages[self.id] = self
            setKey(f"/messages/{self.id}/message.json", self.toJSONSimple())
        for callback in Message.saveCallbacks:
            callback(self)
    
    def delete(self):
        with lock.gen_wlock():
            deleteKey(f"/messages/{self.id}")
            del messages[self.id]
        
    def toJSON(self):
        return {
            "id":        self.id,
            "from":      self.fromUser.toJSON(),
            "to":        self.toUser.toJSON() if self.toUser else {},
            "general":   self.isGeneral,
            "admin":     self.isAdmin,
            "message":   self.message,
            "timestamp": self.timestamp
        }

    def forEach(callback: callable):
        with lock.gen_rlock():
            for id in messages:
                callback(messages[id])
    
    def onSave(callback: callable):
        Message.saveCallbacks.append(callback)
    
    def messagesSince(timestamp: float) -> list:
        with lock.gen_rlock():
            return [messages[id] for id in messages if messages[id].timestamp >= timestamp]

with lock.gen_wlock():
    for id in listSubKeys("/messages"):
        messages[id] = Message(id)
