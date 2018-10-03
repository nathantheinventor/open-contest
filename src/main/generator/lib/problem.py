from .htmllib import *
from .page import Card, Page
from ..db import getKey

languages = [
    ("Python 2", "python"),
    ("Python 3", "python"),
    ("C++", "c_cpp")
]
def languageElem(language):
    dispName, aceName = language
    return h.option(dispName, value=aceName)

class CodeEditor(UIElement):
    def __init__(self):
        self.html = div(cls="code-editor card", contents=[
            div(cls="card-header", contents=[
                h2("Code Editor", cls="card-title"),
                h.select(cls="language-picker", contents=map(languageElem, languages))
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
    
    def listElem(self):
        return Card(self.title, self.description, "/static/problems/{}.html".format(self.guid))

    def descriptionPage(self):
        return str(Page(
            h2(self.title, cls="page-title"),
            div(cls="problem-description", contents=[
                Card("Problem Statement", self.statement),
                Card("Input Format", self.input),
                Card("Output Format", self.output),
                Card("Constraints", self.constraints)
            ]),
            CodeEditor()
        ))
