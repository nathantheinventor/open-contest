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
        Card("Contests", "Create contests", "/static/contests.html"),
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

def generateContestsPage():
    generate("contests.html", Page(
        h2("Contests", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Create Contest", cls="create-contest")
        ]),
        div(cls="contest-cards")
    ))

def generateContestPage():
    generate("contest.html", Page(
        h2("Contest", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Choose Problem", cls="choose-problem")
        ]),
        Card("Contest Details", div(cls="contest-details", contents=[
            h.form(cls="row", contents=[
                div(cls="form-group col-12", contents=[
                    h.label(**{"for": "contest-name", "contents":"Name"}),
                    h.input(cls="form-control", name="contest-name", id="contest-name")
                ]),
                div(cls="form-group col-6", contents=[
                    h.label(**{"for": "contest-start-date", "contents":"Start Date"}),
                    h.input(cls="form-control", name="contest-start-date", id="contest-start-date", type="date")
                ]),
                div(cls="form-group col-6", contents=[
                    h.label(**{"for": "contest-start-time", "contents":"Start Time"}),
                    h.input(cls="form-control", name="contest-start-time", id="contest-start-time", type="time")
                ]),
                div(cls="form-group col-6", contents=[
                    h.label(**{"for": "contest-end-date", "contents":"End Date"}),
                    h.input(cls="form-control", name="contest-end-date", id="contest-end-date", type="date")
                ]),
                div(cls="form-group col-6", contents=[
                    h.label(**{"for": "contest-end-time", "contents":"End Time"}),
                    h.input(cls="form-control", name="contest-end-time", id="contest-end-time", type="time")
                ])
            ])
        ])),
        div(cls="problem-cards")
    ))


# Generate static files needed for overall functioning
def generateStatic():
    generateLogin()
    generateSetup()
    generateInitialProblems()
    generateInitialLeaderboard()
    generateUsersPage()
    generateContestsPage()
    generateContestPage()

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
    