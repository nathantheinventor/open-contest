from htmllib import *

class Problem(UIElement):
    def __init__(self, title, url, description):
        self.html = a(cls="problem-link", href=url, contents=[
            div(cls="problem", contents=[
                div(title, cls="problem-title"),
                div(description, cls="problem-description")
            ])
        ])

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