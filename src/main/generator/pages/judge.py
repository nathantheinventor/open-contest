from code.util import register
from code.util.db import Contest, Problem, Submission
from code.generator.lib.htmllib import *
from code.generator.lib.page import *

class ProblemTab(UIElement):
    def __init__(self, x):
        num, prob = x
        self.html = h.li(
            h.a(prob.title, href=f"#tabs-{num}")
        )

class SubmissionCard(UIElement):
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

class ProblemContent(UIElement):
    def __init__(self, x, cont):
        num, prob = x
        subs = filter(lambda sub: sub.problem == prob and cont.start <= sub.timestamp <= cont.end, Submission.all())
        self.html = div(*map(SubmissionCard, subs), id=f"tabs-{num}")

def judge(params, user):
    cont = Contest.getCurrent()
    if not cont:
        return ""
    
    problemTabs = [*map(ProblemTab, enumerate(cont.problems))]
    problemContents = [*map(lambda x: ProblemContent(x, cont), enumerate(cont.problems))]
    return Page(
        h2("Judge Submissions", cls="page-title"),
        div(id="judge-tabs", contents=[
            h.ul(*problemTabs),
            *problemContents
        ])
    )

register.web("/judge", "admin", judge)