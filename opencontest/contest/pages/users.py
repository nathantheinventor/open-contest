from django.http import HttpResponse

from contest.auth import admin_required
from contest.models.user import User
from contest.pages.lib import Card, Page
from contest.pages.lib.htmllib import UIElement, div, h, h2


class UserCard(UIElement):
    def __init__(self, user: User):
        cls = "blue" if user.isAdmin() else ""
        self.html = div(cls="col-3", contents = [
            Card(
                div(
                    h.strong(h.i("Username:"), cls="username-hidden"),
                    h.br(cls="username-hidden"),
                    h.p("&quot;", cls="username-hidden"),
                    h2(user.username, cls="card-title"),
                    h.p("&quot;", cls="username-hidden")
                ),
                div(
                    h.strong(h.i("Password:")),
                    h.br(),
                    f"&quot;{user.password}&quot;"
                ),
                delete=f"deleteUser('{user.username}')",
                cls=cls
            )
        ])


@admin_required
def getUsers(request):
    userLists = []
    tmp = []
    
    for user in User.all():
        tmp.append(user)
        if len(tmp) == 16:
            userLists.append(tmp)
            tmp = []
    
    if tmp != []:
        userLists.append(tmp)
    
    users = []
    for lst in userLists:
        users.append(div(*map(UserCard, lst), cls="page-break row"))

    return HttpResponse(Page(
        h2("Users", cls="page-title"),
        div(cls="actions", contents=[
            h.button("+ Create Admin", cls="button button-blue create-admin", onclick="createUser('admin')"),
            h.button("+ Create Participant", cls="button create-participant", onclick="createUser('participant')")
        ]),
        div(cls="user-cards", contents=users)
    ))
