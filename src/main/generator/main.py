from .lib import Problem, Page, Card
from .lib.htmllib import *
from .db import listSubKeys, ensureExists

def generate(path, contents):
    ensureExists("/code/serve/" + path)
    with open("/code/serve/" + path, "w") as f:
        f.write(str(contents))

def generateLogin():
    generate("login.html", Page(
        div(cls="login-box", contents=[
            h2("Login", cls="login-header"),
            h.label("Username", cls="form-label"),
            h.input(name="username", cls="form-control"),
            h.label("Password", cls="form-label"),
            h.input(name="password", cls="form-control", type="password"),
            div(cls="align-right", contents=[
                h.button("Login", cls="login-button")
            ])
        ])
    ))

def generateSetup():
    generate("setup.html", Page(
        h2("Setup", cls="page-title"),
        Card("Contests", "Create contests", "/static/createContests.html"),
        Card("Users", "Create users who will participate in contests, as well as other admin users who can create and judge contests and problems", "/static/users.html")
    ))

def generateInitialProblems():
    generate("problems.html", Page(
        h1("No problems available yet")
    ))

def generateInitialLeaderboard():
    generate("leaderboard.html", Page(
        h1("Leaderboard not available yet")
    ))

def generateUsersPage():
    generate("users.html", Page(
        h2("Users", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Create Admin", cls="button-blue create-admin"),
            h.button("+ Create Participant", cls="create-participant")
        ]),
        div(cls="row user-cards")
    ))

# Generate static files needed for overall functioning
def generateStatic():
    generateLogin()
    generateSetup()
    generateInitialProblems()
    generateInitialLeaderboard()
    generateUsersPage()

problemList = []

def generateProblemsPage():
    for problem in problemList:
        generate("problems/{}.html".format(problem.guid), problem.descriptionPage())
    generate("problems.html", Page(
        h.h2("Problems", cls="page-title"),
        *map(lambda x: x.listElem(), problemList)
    ))

def generateProblems():
    global problemList
    problemIds = listSubKeys("/problems")
    curProblems = [Problem(id) for id in problemIds]
    if curProblems != problemList:
        problemList = curProblems
        generateProblemsPage()

# Generate dynamic files that change occasionally, such as problem statements
# Called once per second
def generateDynamic():
    generateProblems()
    