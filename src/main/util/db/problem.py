from code.util.db import getKey, setKey, listSubKeys, deleteKey

problems = {}

class Datum:
    def __init__(self, input, output):
        self.input = input
        self.output = output
    
    def get(id: str, num: int):
        input = getKey(f"/problems/{id}/input/in{num}.txt")
        output = getKey(f"/problems/{id}/output/out{num}.txt")
        return Datum(input, output)
    
    def toJSON(self):
        return {
            "input": self.input,
            "output": self.output
        }

class Problem:
    def __init__(self, id):
        details = getKey(f"/problems/{id}/problem.json")
        self.id          = details["id"]
        self.title       = details["title"]
        self.description = details["description"]
        self.statement   = details["statement"]
        self.input       = details["input"]
        self.output      = details["output"]
        self.constraints = details["constraints"]
        self.samples     = int(details["samples"])
        self.tests       = int(details["tests"])
        self.sampleData  = [Datum.get(id, i) for i in range(self.samples)]
        self.testData    = [Datum.get(id, i) for i in range(self.tests)]

    def get(id: str):
        if id in problems:
            return problems[id]
        return None
    
    def toJSONSimple(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "statement":   self.statement,
            "input":       self.input,
            "output":      self.output,
            "constraints": self.constraints,
            "samples":     self.samples,
            "tests":       self.tests,
        }

    def save(self):
        setKey(f"/problems/{self.id}/problem.json", self.toJSONSimple())
        for i, datum in enumerate(self.testData):
            setKey(f"/problems/{self.id}/input/in{i}.txt", datum["input"])
            setKey(f"/problems/{self.id}/output/out{i}.txt", datum["output"])
    
    def delete(self):
        deleteKey(f"/problems/{self.id}")
        
    def toJSON(self):
        json = self.toJSONSimple()
        json.sampleData = [datum.toJSON() for datum in self.sampleData]
        return json
    
    def toJSONFull(self):
        json = self.toJSONSimple()
        json.testData = [datum.toJSON() for datum in self.testData]
        return json

for id in listSubKeys("/problems"):
    problems[id] = Problem(id)
