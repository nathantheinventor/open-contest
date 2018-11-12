from code.util.db import Submission
from .static import generate
from code.generator.lib.htmllib import *
from code.generator.lib.page import *

class SubmissionDisplay(UIElement):
    def __init__(self, submission: Submission):
        subTime = submission.timestamp * 1000
        probName = submission.problem.title
        cls = "red" if submission.result != "ok" else ""
        self.html = Card("Submission to {} at <span class='time-format'>{}</span>".format(probName, subTime), [
            h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
            h.br(),
            h.strong("Result: <span class='result-format'>{}</span>".format(submission.result)),
            h.br(),
            h.br(),
            h.strong("Code:"),
            h.code(submission.code.replace("\n", "<br/>").replace(" ", "&nbsp;"))
        ], cls=cls)

submissions = {}

def generateSubmission(sub):
    # Add submission to the list of submissions for this user
    user = sub.user.id
    if user not in submissions:
        submissions[user] = {sub}
    submissions[user].add(sub)

    # Sort the submissions from newest to oldest
    subs = sorted(submissions[user], key=lambda sub: sub.timestamp, reverse=True)

    generate(f"/submissions/{user}.html", Page(
        h2("Your Submissions", cls="page-title"),
        *map(SubmissionDisplay, subs)
    ))

def generateSubmissions():
    Submission.forEach(generateSubmission)
    Submission.onSave(generateSubmission)
