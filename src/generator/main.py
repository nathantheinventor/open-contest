from page import Page, Card
from problem import Problem as ProblemUI
from problem import CodeEditor
from htmllib import *
from storage import *
import os

PORT = 8000

from uuid import uuid4
class Problem:
    # def __init__(self, title, description, statement, input, output, constraints):
    #     self.title       = title
    #     self.description = description
    #     self.guid        = str(uuid4())
    #     self.statement   = statement
    #     self.input       = input
    #     self.output      = output
    #     self.constraints = constraints
    def __init__(self, guid):
        settings = getDBFile("problems/{}.json".format(guid))
        self.title       = settings["title"]
        self.description = settings["description"]
        self.guid        = guid
        self.statement   = settings["statement"]
        self.input       = settings["input"]
        self.output      = settings["output"]
        self.constraints = settings["constraints"]
    
    def listElem(self):
        return Card(self.title, self.description, "/problems/{}.html".format(self.guid))

    def descriptionPage(self):
        return str(Page(
            h2(self.title, cls="page-title"),
            div(cls="problem-description", contents=[
                Card("Problem Statement", self.statement),
                Card("Input Format", self.input),
                Card("Output Format", self.output),
                Card("Constraints", self.constraints)
            ]),
            CodeEditor()
        ))

class Contest:
    # def __init__(self, title, description, problems):
    #     self.title       = title
    #     self.description = description
    #     self.guid        = str(uuid4())
    #     self.problems    = problems

    def __init__(self, guid):
        settings = getDBFile("contests/{}.json".format(guid))
        self.title       = settings["title"]
        self.description = settings["description"]
        self.guid        = guid
        self.problems    = [Problem(guid) for guid in settings["problems"]]
    
    def listElem(self):
        return Card(self.title, self.description, "/contests/{}.html".format(self.guid))

    def descriptionPage(self):
        return str(Page(
            h2(self.title, cls="page-title"),
            p(self.description, cls="details"),
            *map(lambda x: x.listElem(), self.problems)
        ))



# prob1 = Problem("Square Numbers", "Find the square of a number given to you", "Given a number x, find x^2", "An integer x", "The number x^2", "1 <= x <= 10^10")
# prob2 = Problem("Cube Numbers", "Find the cube of a number given to you", "Given a number x, find x^3", "An integer x", "The number x^3", "1 <= x <= 10^10")
# prob3 = Problem("Quartic Numbers", "Find the fourth power of a number given to you", "Given a number x, find x^4", "An integer x", "The number x^4", "1 <= x <= 10^10")

# problems = [
#     prob1,
#     prob2,
#     prob3
# ]

# contests = [
#     Contest("Nathan's Contest", "A contest for Nathan the coder", [prob1, prob2]),
#     Contest("Sam's Contest", "A contest for Sam the monkey", [prob1, prob3])
# ]

def generate(data):
    problems = listProblems()
    contests = listContests()
    print(problems, contests)
    problems = [Problem(x) for x in problems]
    contests = [Contest(x) for x in contests]
    try:
        os.mkdir("/tmp/serve")
        os.mkdir("/tmp/serve/problems")
        os.mkdir("/tmp/serve/contests")
    except:
        pass

    with open("/tmp/serve/problems.html", "w") as f:
        f.write(str(Page(
            h.h2("Problems", cls="page-title"),
            *map(lambda x: x.listElem(), problems)
        )))
    
    with open("/tmp/serve/index.html", "w") as f:
        f.write(str(Page(
            h.h2("Problems", cls="page-title"),
            *map(lambda x: x.listElem(), problems)
        )))

    with open("/tmp/serve/contests.html", "w") as f:
        f.write(str(Page(
            h.h2("Contests", cls="page-title"),
            *map(lambda x: x.listElem(), contests)
        )))

    uploadHTMLFile("index.html")
    uploadHTMLFile("problems.html")
    uploadHTMLFile("contests.html")

    for problem in problems:
        with open("/tmp/serve/problems/{}.html".format(problem.guid), "w") as f:
            f.write(problem.descriptionPage())
        uploadHTMLFile("problems/{}.html".format(problem.guid))

    for contest in contests:
        with open("/tmp/serve/contests/{}.html".format(contest.guid), "w") as f:
            f.write(contest.descriptionPage())
        uploadHTMLFile("contests/{}.html".format(contest.guid))

if __name__ == "__main__":
    generate({})
