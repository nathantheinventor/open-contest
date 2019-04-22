from code.util import register, auth
import time

def root(params, setHeader, user):
    setHeader("Location", "/problems")
    return 302

def login(params, setHeader, user):
    username = params["username"]
    password = params["password"]
    user = auth.checkPassword(username, password)
    if user:
        setHeader("Set-Cookie", f"user={user.id}")
        setHeader("Set-Cookie", f"userType={user.type}")
        setHeader("Set-Cookie", f"userLoginTime={time.time() * 1000}")
        return "ok"
    else:
        return "Incorrect username / password";

def logout(params, setHeader, user):
    setHeader("Location", "/login")
    setHeader("Set-Cookie", "user=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT;")
    setHeader("Set-Cookie", "userType=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    return 302

register.get("/", "loggedin", root)
register.post("/login", "any", login)
register.get("/logout", "any", logout)
