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

class FAQ(UIElement):
    def __init__(self, q, a):
        id = str(uuid())
        self.html = div(
            h.h4(q, cls="qa-question collapsed", **{"data-toggle": "collapse", "data-target": f"#qa-{id}"}),
            div(a, id=f"qa-{id}", cls="collapse"),
            cls="faq"
        )

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
    generate("faqs.html", Page(
        h2("FAQs", cls="page-title"),
        FAQ("What is a programming contest?", """A programming contest is a contest where programmers 
            attempt to solve problems by writing programs. These problems are typically posed as a 
            problem statement to describe the problem, input that the program must process, and 
            output that the program must produce. The goal of solving the problem is to write a 
            program that produces the same output for a given input as the judge's solution."""),
        FAQ("What happens when I submit to a problem?", """When you submit code to a problem, 
            your code is automatically run against secret test data and judged based on the output
            it produces. Your code can recieve the following verdicts:
            <ul><li><i>Accepted</i>: Your code produced the correct output for all test cases.</li>
                <li><i>Wrong Answer</i>: Your code produced incorrect output for some test case.</li>
                <li><i>Runtime Error</i>: Your code threw an exception and exited with a non-zero exit code.</li>
                <li><i>Time Limit Exceeded</i>: Your code ran longer than the time allowed.</li></ul>
            """),
        FAQ("How does scoring work?", """Your score is determined by two factors: the number of problems 
            you solve and the number of penalty points you accrue. Contestants are ranked first on 
            problems solved, so a contestant who solves 5 problems will always rank higher than a 
            contestant who solves 4 problems, without regard to the penalty points, but two contestants 
            who each solve 4 problems will be ranked against each other by penalty points.<br/><br/>
            Penalty points are determined by the time it takes you to solve the problems and the number 
            of incorrect submissions that you make. When you solve a problem, you accrue 1 penalty point 
            for each minute that it has been from the beginning of the contest and 20 penalty points 
            for each incorrect submission you made to that problem. For example, if you solve a problem 
            137 minutes into the contest after making 2 incorrect submissions, you will accrue 177 
            penalty points. You do not accrue penalty points for incorrect submissions to a problem 
            if you never solve that problem.<br/><br/>
            For example, if Jim and Bob solve problems at the following times:<br/><br/>
            <table>
                <thead><tr><th>Problem</th>
                    <th class="center">1</th><th class="center">2</th><th class="center">3</th>
                    <th class="center">4</th><th class="center">5</th></tr></thead>
                <tbody>
                    <tr><td>Jim</td>
                        <td class="center">37 minutes,<br/>1 wrong<br/>57 points</td>
                        <td class="center">14 minutes,<br/>2 wrong<br/>54 points</td>
                        <td class="center">43 minutes,<br/>0 wrong<br/>43 points</td>
                        <td class="center"><br/>5 wrong<br/>0 points</td>
                        <td class="center">59 minutes,<br/>1 wrong<br/>79 points</td>
                    </tr>
                    <tr><td>Bob</td>
                        <td class="center">7 minutes,<br/>0 wrong<br/>7 points</td>
                        <td class="center">23 minutes,<br/>1 wrong<br/>43 points</td>
                        <td class="center"><br/><br/>0 points</td>
                        <td class="center">53 minutes,<br/>2 wrong<br/>93 points</td>
                        <td class="center">41 minutes,<br/>1 wrong<br/>61 points</td>
                    </tr>
                </tbody>
            </table><br/>
            Jim will receive a total of 233 points, and Bob will receive a total of 204 points,
            so Bob, having fewer penalty points, will rank above Jim.
            """),
        FAQ("Why am I getting Runtime Error?", """Here are a few tips:
            <ul><li>Check for anywhere that your code could divide by zero.</li>
                <li>Check for the index being out of bounds on an array.</li>
                <li>Check for excessive recursion in Python. Python allows only a small number of
                    recursive calls to a function</li>
                <li>Check that your program's exit code is zero. In C/C++, the main function should
                    return 0.</li>
                </ul>"""),
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