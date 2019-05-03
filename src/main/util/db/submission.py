from code.util.db import getKey, setKey, listSubKeys, deleteKey, User, Problem
from uuid import uuid4
import logging
from readerwriterlock import rwlock
import os.path

lock = rwlock.RWLockWrite()

submissions = {}

class Submission:

    MAX_OUTPUT_LEN = 10000000
    MAX_DISPLAY_OUTPUT_LEN = 10000

    saveCallbacks = []
    def __init__(self, id=None):
        if id != None:
            details = getKey(f"/submissions/{id}/submission.json")
            self.id          = details["id"]
            self.user        = User.get(details["user"])
            self.problem     = Problem.get(details["problem"])
            self.timestamp   = int(details["timestamp"])
            self.language    = details["language"]
            self.code        = details["code"]
            self.type        = details["type"]
            self.results     = details["results"]
            self.inputs      = details["inputs"]
            self.outputs     = details["outputs"]
            self.errors      = details["errors"]
            self.answers     = details["answers"]
            self.result      = details["result"]
            self.status      = details.get("status", None)
            self.checkout    = details.get("checkout", None)
            self.version     = details.get("version", 1)
        else:
            self.id          = None
            self.user        = None
            self.problem     = None
            self.timestamp   = 0
            self.language    = None
            self.code        = None
            self.type        = None
            self.results     = []
            self.inputs      = []
            self.outputs     = []
            self.errors      = []
            self.answers     = []
            self.result      = []
            self.status      = None
            self.checkout    = None
            self.version     = 1

    def get(id: str):
        with lock.gen_rlock():
            if id in submissions:
                return submissions[id]
        return None
    
    def toJSONSimple(self):
        return {
            "id":        self.id,
            "user":      self.user.id,
            "problem":   self.problem.id,
            "timestamp": self.timestamp,
            "language":  self.language,
            "code":      self.code,
            "type":      self.type,
            "results":   self.results,
            "inputs":    self.inputs,
            "outputs":   self.outputs,
            "errors":    self.errors,
            "answers":   self.answers,
            "result":    self.result,
            "status":    self.status,
            "checkout":  self.checkout,
            "version":   self.version,
        }

    def getContestantResult(self):
        return "pending_review" if self.result != "pending" and self.status == "Review" else self.result

    def getContestantIndividualResults(self):
        return ["pending_review" if self.result != "pending" and self.status == "Review" else res for res in self.results]

    def save(self):
        with lock.gen_wlock():
            if self.id == None:
                self.id = str(uuid4())
                submissions[self.id] = self
            full_outputs = []
            for i in range(len(self.outputs)):
                full_output = self.outputs[i] 
                if full_output == None:
                    full_output = ""
                full_outputs.append(full_output)
                if len(full_output) > Submission.MAX_DISPLAY_OUTPUT_LEN:
                    self.outputs[i] = full_output[:Submission.MAX_DISPLAY_OUTPUT_LEN] + "\n... additional output not shown..."

            setKey(f"/submissions/{self.id}/submission.json", self.toJSONSimple())
            if not os.path.exists(f"/db/submissions/{self.id}/output0.txt"):
                for i in range(len(self.outputs)):
                    with open(f"/db/submissions/{self.id}/output{i}.txt", "w") as f:
                        f.write(full_outputs[i])

        for callback in Submission.saveCallbacks:
            callback(self)
    
    def delete(self):
        with lock.gen_wlock():
            if self.id is not None and self.id in submissions:
                deleteKey(f"/submissions/{self.id}")
                del submissions[self.id]
        
    def toJSON(self):
        with lock.gen_rlock():
            #logging.info(self.__dict__.keys())
            if "compile" in self.__dict__:
                return {
                    "id":        self.id,
                    "user":      self.user.id,
                    "problem":   self.problem.id,
                    "timestamp": self.timestamp,
                    "language":  self.language,
                    "code":      self.code,
                    "type":      self.type,
                    "compile":   self.compile,
                    "results":   self.results
                }
            
            
            return {
                "id":        self.id,
                "user":      self.user.id,
                "problem":   self.problem.id,
                "timestamp": self.timestamp,
                "language":  self.language,
                "code":      self.code,
                "type":      self.type,
                "results":   self.results,
                "inputs":    self.inputs [:self.problem.samples] if self.type != "custom" else self.inputs,
                "outputs":   self.outputs[:self.problem.samples] if self.type != "custom" else self.outputs,
                "errors":    self.errors [:self.problem.samples] if self.type != "custom" else self.errors,
                "answers":   self.answers[:self.problem.samples] if self.type != "custom" else self.answers,
                "result":    self.result,
                "status":    self.status,
                "checkout":  self.checkout,
                "version":   self.version,
            }

    def forEach(callback: callable):
        with lock.gen_rlock():
            for id in submissions:
                callback(submissions[id])
    
    def onSave(callback: callable):
        Submission.saveCallbacks.append(callback)
    
    def all():
        with lock.gen_rlock():
            return [submissions[id] for id in submissions]

with lock.gen_wlock():
    for id in listSubKeys("/submissions"):
        submissions[id] = Submission(id)
