import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from contest.auth import logged_in_required, checkPassword
from contest.pages.lib import Page
from contest.pages.lib.htmllib import div, h2, h


@logged_in_required
def root(request):
    return HttpResponseRedirect('/problems')


def login(request):
    if request.method == 'GET':
        return HttpResponse(Page(
            div(cls="login-box", contents=[
                h2("Login", cls="login-header"),
                h.label("Username", cls="form-label"),
                h.input(name="username", cls="form-control"),
                h.label("Password", cls="form-label"),
                h.input(name="password", cls="form-control", type="password"),
                div(cls="align-right", contents=[
                    h.button("Login", cls="button login-button")
                ])
            ])
        ))
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = checkPassword(username, password)
        if user:
            resp = JsonResponse('ok', safe=False)
            resp.set_cookie('user', user.id)
            resp.set_cookie('userType', user.type)
            resp.set_cookie('userLoginTime', time.time() * 1000)
            return resp
        else:
            return JsonResponse('Incorrect username / password', safe=False)


def logout(request):
    resp = HttpResponseRedirect('/login')
    resp.set_cookie('user', 'deleted', expires='Thu, 01 Jan 1970 00:00:00 GMT;')
    resp.set_cookie('userType', 'deleted', expires='Thu, 01 Jan 1970 00:00:00 GMT;')
    return resp

