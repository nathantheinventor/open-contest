import json

from django.http import JsonResponse

from contest.auth import admin_required
from contest.models.problem import Datum, Problem


@admin_required
def deleteProblem(request):
    id = request.POST["id"]
    Problem.get(id).delete()
    return JsonResponse("ok", safe=False)


@admin_required
def createProblem(request):
    id = request.POST.get("id")
    problem = Problem.get(id) or Problem()

    problem.title = request.POST["title"]
    problem.description = request.POST["description"]
    problem.statement = request.POST["statement"]
    problem.input = request.POST["input"]
    problem.output = request.POST["output"]
    problem.constraints = request.POST["constraints"]
    problem.samples = int(request.POST["samples"])

    testData = json.loads(request.POST["testData"])
    problem.testData = [Datum(d["input"], d["output"]) for d in testData]
    problem.tests = len(testData)
    problem.timelimit = request.POST["timelimit"]

    problem.save()

    return JsonResponse(problem.id, safe=False)
