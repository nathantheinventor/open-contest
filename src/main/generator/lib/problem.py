from .htmllib import *
from .page import Card, Page
from ..db import getKey
import markdown2

def formatMD(md: str) -> str:
    """ Convert Markdown to HTML """
    return markdown2.markdown(md)

# languages = [
#     ("C", "c"),
#     ("C++", "cpp"),
#     ("C#", "cs"),
#     ("Java", "java"),
#     ("Python 2", "python2"),
#     ("Python 3", "python3"),
#     ("Ruby", "ruby"),
#     ("Visual Basic", "vb")
# ]
# def languageElem(language):
#     dispName, aceName = language
#     return h.option(dispName, value=aceName)

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

class Problem:
    def __init__(self, guid):
        problem = getKey("/problems/{}/problem.json".format(guid))
        self.title       = problem["title"]
        self.description = problem["description"]
        self.guid        = guid
        self.statement   = problem["statement"]
        self.input       = problem["input"]
        self.output      = problem["output"]
        self.constraints = problem["constraints"]
        self.samples     = int(problem["samples"])
    
    def listElem(self):
        return Card(self.title, self.description, "/static/problems/{}.html".format(self.guid))

    def getSample(self, n: int) -> Card:
        inp = getKey("/problems/{}/input/in{}.txt".format(self.guid, n))
        outp = getKey("/problems/{}/output/out{}.txt".format(self.guid, n))
        return Card("Sample #{}".format(n), div(cls="row", contents=[
            div(cls="col-6", contents=[
                h.p("Input:", cls="no-margin"),
                h.code(inp.replace("\n", "<br/>").replace(" ", "&nbsp;"))
            ]),
            div(cls="col-6", contents=[
                h.p("Output:", cls="no-margin"),
                h.code(outp.replace("\n", "<br/>").replace(" ", "&nbsp;"))
            ])
        ]))

    def descriptionPage(self):
        return str(Page(
            h.input(type="hidden", id="problem-id", value=self.guid),
            h2(self.title, cls="page-title"),
            div(cls="problem-description", contents=[
                Card("Problem Statement", formatMD(self.statement), cls="stmt"),
                Card("Input Format", formatMD(self.input), cls="inp"),
                Card("Output Format", formatMD(self.output), cls="outp"),
                Card("Constraints", formatMD(self.constraints), cls="constraints"),
                div(cls="samples", contents=list(map(self.getSample, range(self.samples))))
            ]),
            CodeEditor(),
            div(cls="align-right", contents=[
                h.button("Test Code", cls="button test-samples button-white"),
                h.button("Submit Code", cls="button submit-problem")
            ])
        ))
