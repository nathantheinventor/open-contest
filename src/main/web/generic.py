from code.util import register, auth

def submissions(params, setHeader, user):
    setHeader("Location", f"/static/submissions/{user.id}.html")
    return 302

def root(params, setHeader, user):
    setHeader("Location", "/static/problems.html")
    return 302

def login(params, setHeader, user):
    username = params["username"]
    password = params["password"]
    user = auth.checkPassword(username, password)
    if user:
        setHeader("Set-Cookie", f"user={user.id}")
        setHeader("Set-Cookie", f"userType={user.type}")
        return "ok"
    else:
        return "Incorrect username / password";

def logout(params, setHeader, user):
    setHeader("Location", "/static/login.html")
    setHeader("Set-Cookie", "user=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT;")
    setHeader("Set-Cookie", "userType=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    return 302

register.get("/submissions", "loggedin", submissions)
register.get("/", "loggedin", root)
register.post("/login", "any", login)
register.get("/logout", "any", logout)
