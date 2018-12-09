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

icons = {
    "ok": "check",
    "wrong_answer": "times",
    "tle": "clock",
    "runtime_error": "exclamation-triangle"
}
verdict_name = {
    "ok": "Accepted",
    "wrong_answer": "Wrong Answer",
    "tle": "Time Limit Exceeded",
    "runtime_error": "Runtime Error"
}

def resultOptions(result):
    ans = []
    for res in verdict_name:
        if result == res:
            ans.append(h.option(verdict_name[res], value=res, selected="selected"))
        else:
            ans.append(h.option(verdict_name[res], value=res))
    return ans

class TestCaseTab(UIElement):
    def __init__(self, x, sub):
        num, result = x
        self.html = h.li(
            h.a(href=f"#tabs-{sub.id}-{num}", contents=[
                h.i(cls=f"fa fa-{icons[result]}", title=f"{verdict_name[result]}"),
                f"Sample #{num}"
            ])
        )

class TestCaseData(UIElement):
    def __init__(self, x, sub):
        num, input, output, error, answer = x
        self.html = div(id=f"tabs-{sub.id}-{num}", contents=[
            div(cls="row", contents=[
                div(cls="col-12", contents=[
                    h.h4("Input"),
                    h.code(input.replace(" ", "&nbsp;").replace("\n", "<br/>"))
                ])
            ]),
            div(cls="row", contents=[
                div(cls="col-6", contents=[
                    h.h4("Output"),
                    h.code(output.replace(" ", "&nbsp;").replace("\n", "<br/>"))
                ]),
                div(cls="col-6", contents=[
                    h.h4("Correct Answer"),
                    h.code(answer.replace(" ", "&nbsp;").replace("\n", "<br/>"))
                ])
            ])
        ])

class SubmissionCard(UIElement):
    def __init__(self, submission: Submission):
        subTime = submission.timestamp
        probName = submission.problem.title
        cls = "red" if submission.result != "ok" else ""
        self.html = Card("Submission to {} at <span class='time-format'>{}</span>".format(probName, subTime), [
            h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
            h.br(),
            h.strong("Result: ",
                h.select(cls=f"result-choice {submission.id}", onchange=f"changeSubmissionResult('{submission.id}')", contents=[
                    *resultOptions(submission.result)
                ])
            ),
            h.br(),
            h.br(),
            h.strong("Code:"),
            h.code(submission.code.replace("\n", "<br/>").replace(" ", "&nbsp;"), cls="code"),
            div(cls="result-tabs", id="result-tabs", contents=[
                h.ul(*map(lambda x: TestCaseTab(x, submission), enumerate(submission.results))),
                *map(lambda x: TestCaseData(x, submission), zip(range(submission.problem.tests), submission.inputs, submission.outputs, submission.errors, submission.answers))
            ])
        ], cls=cls)

class ProblemContent(UIElement):
    def __init__(self, x, cont):
        num, prob = x
        subs = filter(lambda sub: sub.problem == prob and cont.start <= sub.timestamp <= cont.end, Submission.all())
        self.html = div(*map(SubmissionCard, subs), id=f"tabs-{num}")

def judge(params, user):
    cont = Contest.getCurrent()
    if not cont:
        return Page(
            h1("&nbsp;"),
            h1("No Contest Available", cls="center")
        )
    
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