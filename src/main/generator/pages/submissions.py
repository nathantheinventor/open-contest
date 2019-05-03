from code.util.db import Submission
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util import register
from code.generator.pages.judge import verdict_name, icons
import logging

class SubmissionRow(UIElement):
    def __init__(self, sub):
        result = sub.getContestantResult()
        self.html = h.tr(
            h.td(sub.problem.title),
            h.td(cls='time-format', contents=sub.timestamp),
            h.td(sub.language),
            h.td(
                h.i("&nbsp;", cls=f"fa fa-{icons[result]}"),
                h.span(verdict_name[result])
            ),
            onclick=f"submissionPopupContestant('{sub.id}')"
        )

class SubmissionTable(UIElement):
    def __init__(self, subs):
        self.html = h.table(
            h.thead(
                h.tr(
                    h.th("Problem"),
                    h.th("Time"),
                    h.th("Language"),
                    h.th("Result")
                )
            ),
            h.tbody(
                *map(lambda sub: SubmissionRow(sub), subs)
            ),
            id="mySubmissions"
        )

class SubmissionCard(UIElement):
    def __init__(self, submission: Submission):
        subTime = submission.timestamp
        probName = submission.problem.title
        cls = "gray" if submission.status == "Review" else "red" if submission.result != "ok" else ""
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
                h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
                h.br(),
                h.strong("Result: "),
                verdict_name[submission.getContestantResult()],
                h.br(),
                h.br(),
                h.strong("Code:"),
                h.code(code_encode(submission.code), cls="code"),
            ])
        ])

def getSubmissions(params, user):
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
        SubmissionTable(sorted(submissions, key=lambda sub: (sub.problem.title, -sub.timestamp))),
        div(cls="modal", tabindex="-1", role="dialog", contents=[
            div(cls="modal-dialog", role="document", contents=[
                div(id="modal-content")
            ])
        ])
    )

def contestant_submission(params, user):
    return SubmissionCard(Submission.get(params[0]))

register.web("/submissions", "loggedin", getSubmissions)
register.web("/contestantSubmission/([a-zA-Z0-9-]*)", "loggedin", contestant_submission)
