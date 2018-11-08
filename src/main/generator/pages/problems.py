from code.util.db import Problem
from .static import generate
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
import markdown2

def formatMD(md: str) -> str:
    """ Convert Markdown to HTML """
    return markdown2.markdown(md)

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

def getSample(datum, num: int) -> Card:
    return Card("Sample #{}".format(num), div(cls="row", contents=[
        div(cls="col-6", contents=[
            h.p("Input:", cls="no-margin"),
            h.code(datum.input.replace("\n", "<br/>").replace(" ", "&nbsp;"))
        ]),
        div(cls="col-6", contents=[
            h.p("Output:", cls="no-margin"),
            h.code(datum.output.replace("\n", "<br/>").replace(" ", "&nbsp;"))
        ])
    ]))

def generateProblem(problem: Problem):
    generate(f"/problems/{problem.id}.html", Page(
        h.input(type="hidden", id="problem-id", value=problem.id),
        h2(problem.title, cls="page-title"),
        div(cls="problem-description", contents=[
            Card("Problem Statement", formatMD(problem.statement), cls="stmt"),
            Card("Input Format", formatMD(problem.input), cls="inp"),
            Card("Output Format", formatMD(problem.output), cls="outp"),
            Card("Constraints", formatMD(problem.constraints), cls="constraints"),
            div(cls="samples", contents=list(map(lambda x: getSample(x[0], x[1]), zip(problem.sampleData, range(problem.samples)))))
        ]),
        CodeEditor(),
        div(cls="align-right", contents=[
            h.button("Test Code", cls="button test-samples button-white"),
            h.button("Submit Code", cls="button submit-problem")
        ])
    ))

def generateProblems():
    Problem.forEach(generateProblem)
    Problem.onSave(generateProblem)
