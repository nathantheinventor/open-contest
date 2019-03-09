from django.shortcuts import render
from uuid import uuid4
from opencontest.models import Contest, Person

def render_page(req, template, params:dict):
    params.update({
        "PageTitle": Contest.current() or "Open Contest",
        "guid": uuid4(),
    })
    return render(req, template, params)

def no_contest(req):
    return render_page(req, "opencontest/no_contest.html", {})

def get_person(req):
    if req.user.is_authenticated:
        results = Person.objects.filter(user=req.user)
        if len(results) > 0:
            return results[0]
    return None
