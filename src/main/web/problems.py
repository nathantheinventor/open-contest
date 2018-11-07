from code.util import register
from code.util.db.problem import Problem, Datum
import json

def getProblems(params, setHeader, user):
    return Problem.allJSON()

def getProblem(params, setHeader, user):
    id = params["id"]
    return Problem.get(id).toJSONFull()

def deleteProblem(params, setHeader, user):
    id = params["id"]
    Problem.get(id).delete()
    return "ok"

def editProblem(params, setHeader, user):
    id = params.get("id")
    problem = Problem.get(id) or Problem()

    problem.title       = params["title"]
    problem.description = params["description"]
    problem.statement   = params["statement"]
    problem.input       = params["input"]
    problem.output      = params["output"]
    problem.constraints = params["constraints"]
    problem.samples     = int(params["samples"])

    testData            = json.loads(params["testData"])
    problem.testData    = [Datum(d["input"], d["output"]) for d in testData]
    problem.tests       = len(testData)

    problem.save()

    return problem.id

register.post("/getProblems", "admin", getProblems)
register.post("/getProblem", "admin", getProblem)
register.post("/deleteProblem", "admin", deleteProblem)
register.post("/editProblem", "admin", editProblem)
