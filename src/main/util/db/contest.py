from code.util.db import getKey, setKey, listSubKeys, Problem

contests = {}

class Contest:
    def __init__(self, id):
        details = getKey(f"/problems/{id}/problems.json")
        self.id       = details["id"]
        self.name     = details["name"]
        self.start    = int(details["start"])
        self.end      = int(details["end"])
        self.problems = [Problem.construct(id) for id in details["problems"]]

    def construct(id: str):
        if id in contests:
            return contests[id]
        return None
    
    def toJSONSimple(self):
        return {
            "id": self.id,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "problems": [prob.id for prob in self.problems]
        }

    def save(self):
        setKey(f"/problems/{self.id}/problem.json", self.toJSONSimple())
    
    def toJSON():
        return {
            "id": self.id,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "problems": [prob.toJSONSimple() for prob in self.problems]
        }
    
    def allJSON():
        return [contests[id].toJSON() for id in contests]

for id in listSubKeys("/contests"):
    contests[id] = Contest(id)