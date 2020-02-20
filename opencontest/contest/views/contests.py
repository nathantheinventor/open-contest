import json

from django.http import JsonResponse

from contest.auth import admin_required
from contest.models.contest import Contest
from contest.models.problem import Problem


@admin_required
def deleteContest(request, *args, **kwargs):
    id = request.POST['id']
    Contest.get(id).delete()
    return JsonResponse("ok", safe=False)


@admin_required
def createContest(request):
    """POSTing a freshly-created contest redirects here courtesy of script.js."""
    id = request.POST.get("id")
    contest = Contest.get(id) or Contest()

    contest.name = request.POST.get("name")
    contest.start = int(request.POST.get("start"))
    contest.end = int(request.POST.get("end"))
    contest.scoreboardOff = int(request.POST.get("scoreboardOff"))
    contest.showProblInfoBlocks = request.POST.get("showProblInfoBlocks")
    contest.problems = [Problem.get(id) for id in json.loads(request.POST.get("problems"))]
    if str(request.POST.get("tieBreaker")).lower() == "true":
        contest.tieBreaker = True
    else:
        contest.tieBreaker = False

    contest.save()

    return JsonResponse(contest.id, safe=False)
