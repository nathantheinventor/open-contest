from htmllib import *
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
    def __init__(self, url, title):
        self.html = div(cls="menu-item", contents=[
            a(href=url, contents=[
                title
            ])
        ])

class Menu(UIElement):
    def __init__(self):
        self.html = div(cls="menu", contents=[
            div(cls="menu-items", contents=[
                MenuItem("/problems.html", "Problems"),
                MenuItem("/contests.html", "Contests")
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
                h.link(rel="stylesheet", type="text/css", href="/style.css?" + uuid()),
                h.script(src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
                h.script(src="/script.js?" + uuid()),
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
    def __init__(self, title, contents, link=None):
        self.html = h.div(cls="card", contents=[
            div(cls="card-header", contents=[
                h2(title, cls="card-title")
            ]),
            div(cls="card-contents", contents=contents)
        ])
        if link != None:
            self.html = h.a(self.html, href=link, cls="card-link")
