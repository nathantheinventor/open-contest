from code.util import register
from code.util.db import Message, User
import time

def getMessages(params, setHeader, user):
    timestamp = float(params["timestamp"])
    newTime = time.time() * 1000
    messages = Message.messagesSince(timestamp)
    applicable = [message.toJSON() for message in messages if (message.toUser and message.toUser.id == user.id) or message.isGeneral or (message.isAdmin and user.isAdmin()) or message.fromUser.id == user.id]
    applicable = sorted(applicable, key=lambda msg: msg["timestamp"], reverse=True)
    return {
        "messages": applicable,
        "timestamp": newTime
    }

def sendMessage(params, setHeader, user):
    message = Message()
    message.fromUser = user
    message.message = params["message"]
    message.timestamp = time.time() * 1000
    if user.isAdmin():
        message.toUser = User.get(params["to"])
        message.isGeneral = params["to"] == "general"
    else:
        message.isAdmin = True
    message.save()
    return "ok"

register.post("/getMessages", "loggedin", getMessages)
register.post("/sendMessage", "loggedin", sendMessage)
