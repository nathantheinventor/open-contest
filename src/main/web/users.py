from code.util import register
from code.util.db import User
from code.util.auth import generatePassword
import logging

def getUsers(params, setHeader, user):
    return User.allJSON()

def createUser(params, setHeader, user):
    newPassword = generatePassword()
    user = User(
        None,
        params["username"],
        newPassword,
        params["type"]
    )
    user.save()
    return newPassword

def deleteUser(params, setHeader, user):
    username = params["username"]
    user = User.getByName(username)
    user.delete()
    return "ok"

register.post("/getUsers", "admin", getUsers)
register.post("/createUser", "admin", createUser)
register.post("/deleteUser", "admin", deleteUser)
