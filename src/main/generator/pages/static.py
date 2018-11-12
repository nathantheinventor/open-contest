from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util.db.simple import *

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
                h.button("Login", cls="button login-button")
            ])
        ])
    ))

def generateSetup():
    generate("setup.html", Page(
        h2("Setup", cls="page-title"),
        Card("Problems", "Create problems to go in the contests", "/static/problems_mgmt.html"),
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
            h.button("+ Create Admin", cls="button button-blue create-admin"),
            h.button("+ Create Participant", cls="button create-participant")
        ]),
        div(cls="row user-cards")
    ))

def generateContestsPage():
    generate("contests.html", Page(
        h2("Contests", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Create Contest", cls="button create-contest")
        ]),
        div(cls="contest-cards")
    ))

class Modal(UIElement):
    def __init__(self, title, body, footer):
        # taken from https://getbootstrap.com/docs/4.1/components/modal/
        self.html = div(cls="modal", role="dialog", contents=[
            div(cls="modal-dialog", role="document", contents=[
                div(cls="modal-content", contents=[
                    div(cls="modal-header", contents=[
                        h.h5(title, cls="modal-title"),
                        h.button(**{"type": "button", "class": "close", "data-dismiss": "modal", "arial-label": "close"}, contents=[
                            h.span("&times;", **{"aria-hidden": "true"})
                        ])
                    ]),
                    div(body, cls="modal-body"),
                    div(footer, cls="modal-footer")
                ])
            ])
        ])

def generateContestPage():
    generate("contest.html", Page(
        h2("Contest", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Choose Problem", cls="button", onclick="chooseProblemDialog()")
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
            ]),
            div(cls="align-right col-12", contents=[
                h.button("Save", cls="button", onclick="editContest()")
            ])
        ])),
        Modal(
            "Choose Problem",
            h.select(cls="form-control problem-choice", contents=[
                h.option("-")
            ]),
            div(
                h.button("Cancel", **{"type":"button", "class": "button button-white", "data-dismiss": "modal"}),
                h.button("Add Problem", **{"type":"button", "class": "button", "onclick": "chooseProblem()"})
            )
        ),
        div(cls="problem-cards")
    ))

def generateProblemsMgmtPage():
    generate("problems_mgmt.html", Page(
        h2("Problems", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Create Problem", cls="button create-problem")
        ]),
        div(cls="problem-cards")
    ))

def generateProblemMgmtPage():
    generate("problem.html", Page(
        h2("Problem", cls="page-title"),
        div(cls="actions", contents=[
            h.button("View Problem", cls="button", onclick="viewProblem()"),
            h.button("+ Create Test Data", cls="button", onclick="createTestDataDialog()")
        ]),
        Card("Problem Details", div(cls="problem-details", contents=[
            h.form(cls="row", contents=[
                div(cls="form-group col-12", contents=[
                    h.label(**{"for": "problem-title", "contents":"Title"}),
                    h.input(cls="form-control", name="problem-title", id="problem-title")
                ]),
                div(cls="form-group col-12", contents=[
                    h.label(**{"for": "problem-description", "contents":"Description"}),
                    h.textarea(cls="form-control", name="problem-description", id="problem-description")
                ]),
                div(cls="form-group col-12 rich-text", contents=[
                    h.label(**{"for": "problem-statement", "contents":"Problem Statement"}),
                    h.textarea(cls="form-control", name="problem-statement", id="problem-statement")
                ]),
                div(cls="form-group col-12 rich-text", contents=[
                    h.label(**{"for": "problem-input", "contents":"Input Format"}),
                    h.textarea(cls="form-control", name="problem-input", id="problem-input")
                ]),
                div(cls="form-group col-12 rich-text", contents=[
                    h.label(**{"for": "problem-output", "contents":"Output Format"}),
                    h.textarea(cls="form-control", name="problem-output", id="problem-output")
                ]),
                div(cls="form-group col-12 rich-text", contents=[
                    h.label(**{"for": "problem-constraints", "contents":"Constraints"}),
                    h.textarea(cls="form-control", name="problem-constraints", id="problem-constraints")
                ]),
                div(cls="form-group col-12", contents=[
                    h.label(**{"for": "problem-samples", "contents":"Number of Sample Cases"}),
                    h.input(cls="form-control", type="number", name="problem-samples", id="problem-samples", value="0")
                ]),
            ]),
            div(cls="align-right col-12", contents=[
                h.button("Save", cls="button", onclick="editProblem()")
            ])
          ])),
        Modal(
            "Create Test Data",
            div(
                h.h5("Input"),
                h.textarea(rows="5", cls="test-data-input col-12 monospace margin-bottom"),
                h.h5("Output"),
                h.textarea(rows="5", cls="test-data-output col-12 monospace")
            ),
            div(
                h.button("Cancel", **{"type":"button", "class": "button button-white", "data-dismiss": "modal"}),
                h.button("Add Test Data", **{"type":"button", "class": "button", "onclick": "createTestData()"})
            )
        ),
        div(cls="test-data-cards")
    ))

def generatePrivacyPolicy():
    # Real Privacy Policy
    generate("privacy.html", Page(
        h2("Privacy Policy", cls="page-title"),
        Card("TL;DR", "OpenContest as an organization is too lazy to steal your data (we're busy enough keeping track of our own). " +
            "However, the organizers of your contest may collect any data you submit, " +
            "including your name (which the organizers provide) and any code submissions, which they may use for any purpose."),
        Card("Data collected", 
            div(
                h.span("OpenContest collects the following data:"),
                h.ul(
                    h.li("Your name as provided by the contest organizers"),
                    h.li("Your password as generated by the app"),
                    h.li("Any problem statements written by the contest organizers"),
                    h.li("Any contest details created by the contest organizers"),
                    h.li("Any code submissions by contest participants")
                )
            )
        ),
        Card("Data usage", 
            div(
                h.span("Any data collected by OpenContest may be accessible to"),
                h.ul(
                    h.li("The contest organizers"),
                    h.li("Anyone with access to the server that OpenContest is running on"),
                    h.li("Anyone in the world, though we have tried to eliminate this possibility")
                ),
                h.span("Any data collected in OpenContest is stored in plain text on the server that OpenContest is running on. " +
                    "No data is not sent to the developers of OpenContest.")
            )
        )
    ))

    # Fake privacy policy for laughs
    generate("privacy2.html", Page(
        h2("Privacy Policy", cls="page-title"),
        h1("LOL", cls="jumbotron center"),
        h1("After all, you use Facebook", cls="center")
    ))

    # Instructions about using OpenContest
    generate("Instructions.html", Page(
        h2("Instructions", cls="page-title"),
        h1("DON'T", cls="jumbotron center"),
        h1("Just Don't", cls="center")
    ))

# Generate static files that don't change during the contest
def generateStatic():
    generateLogin()
    generateSetup()
    generateInitialProblems()
    generateInitialLeaderboard()
    generateUsersPage()
    generateContestsPage()
    generateContestPage()
    generateProblemsMgmtPage()
    generateProblemMgmtPage()
    generatePrivacyPolicy()