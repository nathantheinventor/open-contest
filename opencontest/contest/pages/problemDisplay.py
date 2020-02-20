import markdown2
from django.http import HttpResponse, JsonResponse

from contest.auth import logged_in_required
from contest.models.contest import Contest
from contest.models.problem import Problem
from contest.models.submission import Submission
from contest.models.user import User
from contest.pages.lib import Card, Page
from contest.pages.lib.htmllib import UIElement, div, h2, h, code_encode, h1


def formatMD(md: str) -> str:
    """ Convert Markdown to HTML """
    return markdown2.markdown(md, extras=["tables"])


class CodeEditor(UIElement):
    def __init__(self):
        self.html = div(cls="code-editor card", contents=[
            div(cls="card-header", contents=[
                h2("Code Editor", cls="card-title"),
                h.select(cls="language-picker custom-select col-2 custom-select-sm")
            ]),
            div(cls="ace-editor-wrapper", contents=[
                div(id="ace-editor", cls="ace-editor", contents=[
                    "#Some Python code"
                ])
            ])
        ])


class ProblemCard(UIElement):
    def __init__(self, prob: Problem, user: User):
        probpath = f"/problems/{prob.id}"

        btn = f"rejudgeAll('{prob.id}')" if user.isAdmin() else None

        title = prob.title
        if not user.isAdmin():
            # Compute problem status
            icon = ''
            result = ''
            for sub in Submission.all():
                if sub.problem != prob or sub.user != user or sub.status == "Review":
                    continue

                if sub.user == user and "ok" == sub.result:
                    icon = "check"
                    break
                else:
                    icon = "times"

            if icon != '':
                result = f'<i class="fa fa-{icon}"></i> '   

            title = result + title

        self.html = Card(
                title,
                prob.description,
                probpath,
                rejudge=btn
            )


def getSample(datum, num: int) -> Card:
    if datum.input == None: datum.input = "" 
    if datum.output == None: datum.output = "" 
    return Card("Sample #{}".format(num), div(cls="row", contents=[
        div(cls="col-12", contents=[
            h.p("Input:", cls="no-margin"),
            h.code(code_encode(datum.input))
        ]),
        div(cls="col-12", contents=[
            h.p("Output:", cls="no-margin"),
            h.code(code_encode(datum.output))
        ])
    ]))


@logged_in_required
def viewProblem(request, *args, **kwargs):
    problem = Problem.get(kwargs.get('id'))
    user = User.get(request.COOKIES.get('user'))
    
    contest = Contest.getCurrent()
    
    if not problem:
        return JsonResponse(data='', safe=False)

    if not user.isAdmin():
        # Hide the problems till the contest begins for non-admin users
        if not Contest.getCurrent():
            return JsonResponse(data='', safe=False)
        if problem not in Contest.getCurrent().problems:
            return JsonResponse(data='', safe=False)
    contents = []
    if contest == None or contest.showProblInfoBlocks == "On":
        contents = [
                Card("Problem Statement", formatMD(problem.statement), cls="stmt"),
                Card("Input Format", formatMD(problem.input), cls="inp"),
                Card("Output Format", formatMD(problem.output), cls="outp"),
                Card("Constraints", formatMD(problem.constraints), cls="constraints"),                
                ]
    contents.append(div(cls="samples", contents=list(map(lambda x: getSample(x[0], x[1]), zip(problem.sampleData, range(problem.samples))))))
    
    return HttpResponse(Page(
        h.input(type="hidden", id="problem-id", value=problem.id),
        h2(problem.title, cls="page-title"),
        div(cls="problem-description", contents=contents),
        CodeEditor(),
        div(cls="stmt card ui-sortable-handle blk-custom-input", contents=[
            div(cls="card-header", contents=[h2("Custom Input", cls="card-title")]),
            div(cls="card-contents", contents=[h.textarea(id="custom-input", cls="col-12")])
        ]),
        div(cls="align-right",id="custom-code-text", contents=[
            h.input("Custom Input", type="checkbox", id="use-custom-input"),
            h.button("Test Code", cls="button test-samples button-white"),
            h.button("Submit Code", cls="button submit-problem")
        ])
    ))


@logged_in_required
def listProblems(request):
    if Contest.getCurrent():
        contest = Contest.getCurrent()
        probCards = []
        user = User.get(request.COOKIES.get('user'))
        for prob in contest.problems:            
            probCards.append(ProblemCard(prob, user))

        return HttpResponse(Page(
            h2("Problems", cls="page-title"),
            *probCards
        ))
    elif Contest.getFuture():
        contest = Contest.getFuture()
        return HttpResponse(Page(
            h1("&nbsp;"),
            h1("Contest Starts in", cls="center"),
            h1(contest.start, cls="countdown jumbotron center")
        ))
    elif Contest.getPast():
        return HttpResponse(Page(
            h1("&nbsp;"),
            h1("Contest is Over", cls="center")
        ))
    return HttpResponse(Page(
        h1("&nbsp;"),
        h1("No Contest Created", cls="center")
    ))
