from django.shortcuts import redirect

from opencontest.views.problems import *
from opencontest.views.submit import *

def index(req):
    return redirect("/problems")
