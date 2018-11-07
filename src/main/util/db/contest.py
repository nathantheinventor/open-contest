from code.util.db import getKey, setKey, listSubKeys, deleteKey, Problem
from uuid import uuid4
import logging

contests = {}

class Contest:
    def __init__(self, id=None):
        if id != None:
            details       = getKey(f"/contests/{id}/contest.json")
            self.id       = details["id"]
            self.name     = details["name"]
            self.start    = int(details["start"])
            self.end      = int(details["end"])
            self.problems = [Problem.get(id) for id in details["problems"]]
        else:
            self.id = None
            self.name = None
            self.start = None
            self.end = None
            self.problems = None

    def get(id: str):
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
        if self.id == None:
            self.id = str(uuid4())
            contests[self.id] = self
        setKey(f"/contests/{self.id}/contest.json", self.toJSONSimple())
    
    def delete(self):
        deleteKey(f"/contests/{self.id}")
        del contests[self.id]
    
    def toJSON(self):
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
