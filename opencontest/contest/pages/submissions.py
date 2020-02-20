from django.http import HttpResponse

from contest.auth import logged_in_required
from contest.models.contest import Contest
from contest.models.submission import Submission
from contest.models.user import User
from contest.pages.lib import Page
from contest.pages.lib.htmllib import UIElement, h, div, code_encode, h2
from contest.pages.judge import icons, verdict_name


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


@logged_in_required
def getSubmissions(request, *args, **kwargs):
    submissions = []
    
    cont = Contest.getCurrent()
    if not cont:
        return HttpResponse('')

    user = User.get(request.COOKIES['user'])
    Submission.forEach(lambda x: submissions.append(x) if x.user.id == user.id and cont.start <= x.timestamp <= cont.end else None)
    if len(submissions) == 0:
        return HttpResponse(Page(
            h2("No Submissions Yet", cls="page-title"),
        ))
    return HttpResponse(Page(
        h2("Your Submissions", cls="page-title"),
        SubmissionTable(sorted(submissions, key=lambda sub: (sub.problem.title, -sub.timestamp))),
        div(cls="modal", tabindex="-1", role="dialog", contents=[
            div(cls="modal-dialog", role="document", contents=[
                div(id="modal-content")
            ])
        ])
    ))


@logged_in_required
def contestant_submission(request, *args, **kwargs):
    return HttpResponse(SubmissionCard(Submission.get(kwargs.get('id'))))
