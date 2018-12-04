from code.util.db import Submission
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util import register
import logging

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

def getSubmissions(_, __, user, ___):
    submissions = []
    
    cont = Contest.getCurrent()
    if not cont:
        return ""
    
    Submission.forEach(lambda x: submissions.append(x) if x.user.id == user.id and cont.start <= x.timestamp <= cont.end else None)
    if len(submissions) == 0:
        return Page(
            h2("No Submissions Yet", cls="page-title"),
        )
    return Page(
        h2("Your Submissions", cls="page-title"),
        *map(SubmissionDisplay, submissions)
    )

register.web("/submissions", "loggedin", getSubmissions)
