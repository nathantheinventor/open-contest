from .htmllib import *
from datetime import datetime
from uuid import uuid4

def uuid():
    return str(uuid4())

class Header(UIElement):
    def __init__(self):
        self.html = div(cls="header", contents=[
            h1("OpenContest")
        ])

class MenuItem(UIElement):
    def __init__(self, url, title, role="any"):
        self.html = div(role=role, cls="menu-item", contents=[
            a(href=url, contents=[
                title
            ])
        ])

class Menu(UIElement):
    def __init__(self):
        self.html = div(cls="menu", contents=[
            div(cls="menu-items", contents=[
                MenuItem("/static/problems.html", "Problems"),
                MenuItem("/static/leaderboard.html", "Leaderboard"),
                MenuItem("/submissions", "My Submissions", role="participant"),
                MenuItem("/static/setup.html", "Setup", role="admin"),
                MenuItem("/logout", "Logout")
            ])
        ])

class Footer(UIElement):
    def __init__(self):
        self.html = div(cls="footer", contents=[
            h2("Copyright &copy; {} by Nathan Collins".format(datetime.now().year))
        ])

class Page(UIElement):
    def __init__(self, *bodyData):
        self.html = h.html(
            head(
                title("Example Page"),
                h.link(rel="stylesheet", href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css", integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO", crossorigin="anonymous"),
                h.link(rel="stylesheet", href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css"),
                h.link(rel="stylesheet", href="https://fonts.googleapis.com/icon?family=Material+Icons"),
                h.link(rel="stylesheet", href="/static/styles/style.css?" + uuid(), type="text/css"),
                h.script(src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
                h.script(src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"),
                h.script(src="/static/scripts/script.js?" + uuid()),
                h.script(src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.1/ace.js")
            ),
            body(
                Header(),
                Menu(),
                div(*bodyData, cls="main-content"),
                Footer()
            )
        )

class Card(UIElement):
    def __init__(self, title, contents, link=None, cls=None):
        if cls == None:
            cls = "card"
        else:
            cls += " card"
        self.html = h.div(cls=cls, contents=[
            div(cls="card-header", contents=[
                h2(title, cls="card-title")
            ]),
            div(cls="card-contents", contents=contents)
        ])
        if link != None:
            self.html = h.a(self.html, href=link, cls="card-link")
