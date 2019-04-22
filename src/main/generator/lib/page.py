from code.util.db import Contest
from .htmllib import *
from datetime import datetime
from uuid import uuid4

def uuid():
    return str(uuid4())

class Header(UIElement):
    def __init__(self, title):
        self.html = div(cls="top", contents=[
            div(cls="header", contents=[
                h1(title)
            ])
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
                MenuItem("/problems", "Problems"),
                MenuItem("/leaderboard", "Leaderboard"),
                MenuItem("/submissions", "My Submissions", role="participant"),
                MenuItem("/messages/inbox", "Messages"),
                MenuItem("/judge", "Judge", role="admin"),
                MenuItem("/setup", "Setup", role="admin"),
                MenuItem("/logout", "Logout")
            ])
        ])

class Footer(UIElement):
    def __init__(self):
        self.html = div(cls="footer", contents=[
            h2('Copyright &copy; {} by <a href="https://nathantheinventor.com" target="_blank">Nathan Collins</a>'.format(datetime.now().year)),
            div(cls="footer-links", contents=[
                h.span(h.a("Privacy Policy", href="/privacy", target="_blank")),
                h.span(h.a("About", href="https://github.com/nathantheinventor/open-contest/", target="_blank")),
                h.span(h.a("FAQs", href="/faqs", target="_blank"))
            ])
        ])

class Page(UIElement):
    def __init__(self, *bodyData):
        cont = Contest.getCurrent()
        title = cont.name if cont else "OpenContest"
        self.html = h.html(
            head(
                h.title(title),
                h.link(rel="stylesheet", href="/static/lib/fontawesome/css/all.css", type="text/css"),
                h.link(rel="stylesheet", href="/static/lib/bootstrap/css/bootstrap.min.css", type="text/css"),
                h.link(rel="stylesheet", href="/static/lib/jqueryui/jquery-ui.min.css", type="text/css"),
                h.link(rel="stylesheet", href="/static/lib/simplemde/simplemde.min.css", type="text/css"),
                h.link(rel="stylesheet", href="/static/styles/style.css?" + uuid(), type="text/css"),
                h.script(src="/static/lib/jquery/jquery.min.js"),
                h.script(src="/static/lib/bootstrap/js/bootstrap.min.js"),
                h.script(src="/static/lib/jqueryui/jquery-ui.min.js"),
                h.script(src="/static/lib/ace/ace.js"),
                h.script(src="/static/lib/simplemde/simplemde.min.js"),
                h.script(src="/static/scripts/script.js?" + uuid()),
                h.script(src="/static/lib/tablefilter_all_min.js"),
                
                h.script(src="https://cdnjs.cloudflare.com/ajax/libs/jsdiff/4.0.1/diff.js"),
                
            ),
            body(
                Header(title),
                Menu(),
                div(cls="message-alerts"),
                div(*bodyData, cls="main-content"),
                Footer()
            )
        )
    
    def setTitle(title):
        Page.title = title
        from code.generator.pages.static import generateStatic
        generateStatic()

class Card(UIElement):
    def __init__(self, title, contents, link=None, cls=None, delete=None, reply=None):
        if cls == None:
            cls = "card"
        else:
            cls += " card"
        deleteLink = ""
        if delete:
            deleteLink = div(h.i("clear", cls="material-icons"), cls="delete-link", onclick=delete)
        elif reply:
            deleteLink = div("Reply", cls="delete-link", onclick=reply)
        self.html = h.div(cls=cls, contents=[
            div(cls="card-header", contents=[
                h2(title, cls="card-title"),
                deleteLink
            ]),
            div(cls="card-contents", contents=contents)
        ])
        if link != None:
            self.html = div(a(href=link, cls="card-link"), self.html, cls="card-link-box")

class Modal(UIElement):
    def __init__(self, title, body, footer):
        # taken from https://getbootstrap.com/docs/4.1/components/modal/
        self.html = div(cls="modal", role="dialog", contents=[
            div(cls="modal-dialog", role="document", contents=[
                div(cls="modal-content", contents=[
                    div(cls="modal-header", contents=[
                        h.h5(title, cls="modal-title"),
                        h.button(**{"type": "button", "class": "close", "data-dismiss": "modal", "arial-label": "close"}, contents=[
                            h.span("&times;", **{"aria-hidden": "true"})
                        ])
                    ]),
                    div(body, cls="modal-body"),
                    div(footer, cls="modal-footer")
                ])
            ])
        ])
