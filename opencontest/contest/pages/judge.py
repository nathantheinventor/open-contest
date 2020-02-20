from django.http import HttpResponse, JsonResponse

from contest.auth import admin_required
from contest.models.contest import Contest
from contest.models.submission import Submission
from contest.models.user import User
from contest.pages.lib import Page
from contest.pages.lib.htmllib import UIElement, h, div, code_encode, h1, h2


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
    "runtime_error": "exclamation-triangle",
    "presentation_error": "times",
    "extra_output": "times",
    "incomplete_output": "times",
    "reject": "times",
    "pending": "sync",
    "pending_review": "sync",
}
verdict_name = {
    "ok": "Accepted",
    "wrong_answer": "Wrong Answer",
    "tle": "Time Limit Exceeded",
    "runtime_error": "Runtime Error",
    "presentation_error": "Presentation Error",
    "extra_output": "Extra Output",
    "incomplete_output": "Incomplete Output",
    "reject": "Submission Rejected",
    "pending": "Executing ...",
    "pending_review": "Pending Review",
}


def resultOptions(result):
    ans = []
    for res in verdict_name:
        if res == "pending" or res == "pending_review":
            pass  # These should not appear as choices in the dropdown
        elif result == res:
            ans.append(h.option(verdict_name[res], value=res, selected="selected"))
        else:
            ans.append(h.option(verdict_name[res], value=res))
    return ans


def statusOptions(status):
    ans = []
    for stat in ["Review", "Judged"]:
        if status == stat:
            ans.append(h.option((stat), value=stat, selected="selected"))
        else:
            ans.append(h.option((stat), value=stat))
    return ans


class TestCaseTab(UIElement):
    def __init__(self, x, sub):
        num, result = x
        test_label = "Sample" if num < sub.problem.samples else "Judge"
        self.html = h.li(
            h.a(href=f"#tabs-{sub.id}-{num}", contents=[
                h.i(cls=f"fa fa-{icons[result]}", title=f"{verdict_name[result]}"),
                f"{test_label} #{num}"
            ])
        )


class TestCaseData(UIElement):
    def __init__(self, x, sub):
        num, input, output, error, answer = x
        if input == None: input = "" 
        if output == None: output = "" 
        self.html = div(id=f"tabs-{sub.id}-{num}", contents=[
            div(cls="row", contents=[
                div(cls="col-12", contents=[
                    h.h4("Input"),
                    h.code(code_encode(input))
                ])
            ]),
            div(cls="row", contents=[
                div(cls="col-6", contents=[
                    h.h4("Output"),
                    h.code(code_encode(output))
                ]),
                div(cls="col-6", contents=[
                    h.h4("Correct Answer"),
                    h.code(code_encode(answer))
                ])
            ]),
            div(cls="row", contents=[
                div(cls="col-12", contents=[
                    h.h4("Diff"),
                    h.em("Insertions are in <span style=color:darkgreen;background-color:palegreen>green</span>, deletions are in <span style=color:darkred;background-color:#F6B0B0>red</span>"),
                    h.code(id=f"diff-{sub.id}-{num}", contents=[
                        h.script(f"document.getElementById('diff-{sub.id}-{num}').innerHTML = getDiff(`{output.rstrip()}`, `{answer.rstrip()}`)")
                    ])
                ])
            ])
        ])


class SubmissionCard(UIElement):
    def __init__(self, submission: Submission, user, force):
        subTime = submission.timestamp
        probName = submission.problem.title
        cls = "gray" if submission.status == "Review" else "red" if submission.result != "ok" else ""
        submission.checkout = user.id
        self.html = div(cls="modal-content", contents=[
            div(cls=f"modal-header {cls}", contents=[
                h.h5(
                    f"Submission to {probName} at ",
                    h.span(subTime, cls="time-format")
                ),
                """
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>"""
            ]),
            div(cls="modal-body", contents=[
                h.input(type="hidden", id="version", value=f"{submission.version}"),
                h.strong(f"Contestant: {submission.user.username}"), h.br(),
                h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
                h.br(),
                h.strong("Result: ",
                    h.select(cls=f"result-choice {submission.id}", contents=[
                        *resultOptions(submission.result)
                    ])
                ),
                h.strong("&emsp;Status: ",
                    h.select(cls=f"status-choice {submission.id}", contents=[
                        *statusOptions(submission.status)
                    ])
                ),
                h.span("&emsp;"),
                h.button("Save", type="button", onclick=f"changeSubmissionResult('{submission.id}', '{submission.version}')", cls="btn btn-primary"),
                h.br(),
                h.br(),
                h.button("Rejudge", type="button", onclick=f"rejudge('{submission.id}')", cls="btn btn-primary rejudge"),
                h.span(" "),
                h.button("Download", type="button", onclick=f"download('{submission.id}')", cls="btn btn-primary rejudge"),
                h.br(),
                h.br(),
                h.strong("Code:"),
                h.code(code_encode(submission.code), cls="code"),
                div(cls="result-tabs", id="result-tabs", contents=[
                    h.ul(*map(lambda x: TestCaseTab(x, submission), enumerate(submission.results))),
                    *map(lambda x: TestCaseData(x, submission), zip(range(submission.problem.tests), 
                        submission.readFilesForDisplay('in'), submission.readFilesForDisplay('out'), 
                        submission.readFilesForDisplay('error'), submission.readFilesForDisplay('answer')))
                ])
            ])
        ])


class ProblemContent(UIElement):
    def __init__(self, x, cont):
        num, prob = x
        subs = filter(lambda sub: sub.problem == prob and cont.start <= sub.timestamp <= cont.end, Submission.all())
        self.html = div(*map(SubmissionCard, subs), id=f"tabs-{num}")


class SubmissionRow(UIElement):
    def __init__(self, sub):
        checkoutUser = User.get(sub.checkout)
        self.html = h.tr(
            h.td(sub.user.username),
            h.td(sub.problem.title),
            h.td(cls='time-format', contents=sub.timestamp),
            h.td(sub.language),
            h.td(
                h.i("&nbsp;", cls=f"fa fa-{icons[sub.result]}"),
                h.span(verdict_name[sub.result])
            ),
            h.td(sub.status),
            h.td(checkoutUser.username if checkoutUser is not None else "None"),
            id=sub.id,
            cls="submit-row"
        )


class SubmissionTable(UIElement):
    def __init__(self, contest):
        subs = sorted(
            filter(lambda sub: sub.user.type != "admin" and contest.start <= sub.timestamp <= contest.end, Submission.all()),
            key=lambda s: s.timestamp)

        self.html = h.table(
            h.thead(
                h.tr(
                    h.th("Name"),
                    h.th("Problem"),
                    h.th("Time"),
                    h.th("Language"),
                    h.th("Result"),
                    h.th("Status"),
                    h.th("Checkout"),
                )
            ),
            h.tbody(
                *map(lambda sub: SubmissionRow(sub), subs)
            ),
            id="submissions"
        )
        print(self.html)


@admin_required
def judge(request):
    cont = Contest.getCurrent()
    if not cont:
        return HttpResponse(Page(
            h1("&nbsp;"),
            h1("No Contest Available", cls="center")
        ))
    return HttpResponse(Page(
        h2("Judge Submissions", cls="page-title judge-width"),
        div(id="judge-table", cls="judge-width", contents=[
            SubmissionTable(cont)
        ]),
        div(cls="modal", tabindex="-1", role="dialog", contents=[
            div(cls="modal-dialog", role="document", contents=[
                div(id="modal-content")
            ])
        ])
    ))


@admin_required
def judge_submission(request, *args, **kwargs):
    submission = Submission.get(kwargs.get('id'))
    user = User.get(request.COOKIES['user'])
    force = kwargs.get('force') == "force"
    if submission.checkout is not None and not force:
        return f"CONFLICT:{User.get(submission.checkout).username}"
    return HttpResponse(SubmissionCard(submission, user, force))


def judge_submission_close(request):
    submission = Submission.get(request.POST["id"])
    user = User.get(request.COOKIES['user'])
    if submission.version == int(request.POST["version"]):
        if submission.checkout == user.id:
            submission.checkout = None
        submission.save()
    return JsonResponse('ok')
