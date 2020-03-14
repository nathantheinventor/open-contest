import logging
from uuid import uuid4
from readerwriterlock import rwlock

from contest.models.contest import Contest
from contest.models.problem import Problem
from contest.models.simple import getKey, setKey, deleteKey, listSubKeys
from contest.models.user import User

from opencontest.settings import OC_MAX_DISPLAY_LEN, OC_MAX_DISPLAY_LEN, OC_MAX_DISPLAY_LINES


lock = rwlock.RWLockWrite()
submissions = {}


class Submission:

    TYPE_CUSTOM = "custom"  # test with custom input 
    TYPE_SUBMIT = "submit"  # full submission
    TYPE_TEST = "test"    # test only

    # Submission result
    RESULT_PENDING = "pending"
    RESULT_PENDING_REVIEW = "pending_review"
    RESULT_REJECT = "reject"

    # Submission status
    STATUS_REVIEW = "Review"
    STATUS_JUDGED = "Judged"

    saveCallbacks = []

    def __init__(self, id=None):
        if id != None:
            details = getKey(f"/submissions/{id}/submission.json")
            self.id = details["id"]
            self.user = User.get(details["user"])
            self.problem = Problem.get(details["problem"])
            self.timestamp = int(details["timestamp"])
            self.language = details["language"]
            self.code = details["code"]
            self.type = details["type"]
            self.results = details["results"]
            self.result = details["result"]
            self.status = details.get("status", None)
            self.checkout = details.get("checkout", None)
            self.version = details.get("version", 1)
        else:
            self.id = None
            self.user = None     # Instance of User
            self.problem = None     # Instance of Problem
            self.timestamp = 0        # Time of submission
            self.language = None
            self.code = None     # Source code
            self.type = None
            self.results = []
            self.result = []
            self.status = None     # One of Submission.STATUS_REVIEW, Submission.STATUS_JUDGED
            self.checkout = None     # id of judge that has submission checked out
            self.version = 1        # Version number for judge changes to this record

        self.inputs = []      # For display only
        self.outputs = []     # For display only
        self.errors = []      # For display only
        self.answers = []     # For display only
        self.compile = None   # Compile error

    @staticmethod
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
            "result":    self.result,
            "status":    self.status,
            "checkout":  self.checkout,
            "version":   self.version,
        }

    def getContestantResult(self):
        return Submission.RESULT_PENDING_REVIEW if self.result != Submission.RESULT_PENDING and self.status == Submission.STATUS_REVIEW else self.result

    def getContestantIndividualResults(self):
        return [Submission.RESULT_PENDING_REVIEW if self.result != Submission.RESULT_PENDING and self.status == Submission.STATUS_REVIEW else res for res in self.results]

    @staticmethod
    def truncateForDisplay(data: str) -> str:
        """Truncates `data` to maximum of OC_MAX_DISPLAY_LEN bytes and
        OC_MAX_DISPLAY_LINES lines
        """

        if data == None:
            return ''

        truncated = False
        if data and len(data) > OC_MAX_DISPLAY_LEN:
            truncated = True
            data = data[:OC_MAX_DISPLAY_LEN]
            
        lines = data.split('\n')
        if len(lines) > OC_MAX_DISPLAY_LINES:
            lines = lines[:OC_MAX_DISPLAY_LINES]
            data = '\n'.join(lines)
            truncated = True
        
        if truncated:
             data += "...\nadditional data not displayed ..."

        return data

    def readFilesForDisplay(self, fileType: str) -> list:
        results = []
        for i in range(self.problem.tests):
            try:
                # TODO: test paths
                with open(f"../db/submissions/{self.id}/{fileType}{i}.txt") as f:
                    data = f.read(OC_MAX_DISPLAY_LEN + 1)
                    results.append(Submission.truncateForDisplay(data))
            except:
                logging.error(f"Problem reading {fileType} #{i} for submission {self.id}")
                results.append('Error reading data')

        return results

    def checkoutToJudge(self, userid: str, force: bool) -> bool:
        with lock.gen_wlock():
            if self.checkout == None or force:
                self.checkout = userid
                return True
    
        return False        

    def changeResult(self, result: str, status: str, orig_version: int) -> bool:
        with lock.gen_wlock():
            if self.version != orig_version:
                return False

            self.result = result
            self.status = status
            self.version += 1
            self.checkout = None
            return True

    def save(self):
        with lock.gen_wlock():
            if self.id == None:
                c = Contest.getCurrent()
                probNum = 0
                if c:
                    for i, prob in enumerate(c.problems):
                        if prob == self.problem:
                            probNum = i + 1                
                self.id = f"{self.user.username}-{probNum}-{uuid4()}"
                submissions[self.id] = self

            setKey(f"/submissions/{self.id}/submission.json", self.toJSONSimple())

        for callback in Submission.saveCallbacks:
            callback(self)
    
    def delete(self):
        with lock.gen_wlock():
            if self.id is not None and self.id in submissions:
                deleteKey(f"/submissions/{self.id}")
                del submissions[self.id]
        
    def toJSON(self):
        with lock.gen_rlock():
            
            return {
                "id":        self.id,
                "user":      self.user.id,
                "problem":   self.problem.id,
                "timestamp": self.timestamp,
                "language":  self.language,
                "code":      self.code,
                "type":      self.type,
                "results":   self.results,
                "result":    self.result,
                "status":    self.status,
                "checkout":  self.checkout,
                "version":   self.version,
                "compile":   self.compile,
                "inputs":    self.inputs,
                "outputs":   self.outputs,
                "answers":   self.answers,
                "errors":    self.errors
            }

    @staticmethod
    def forEach(callback: callable):
        with lock.gen_rlock():
            for id in submissions:
                callback(submissions[id])
    
    @staticmethod
    def onSave(callback: callable):
        Submission.saveCallbacks.append(callback)

    def __str__(self):
        return str(self.toJSON())

    @staticmethod
    def all():
        """Returns all submissions sorted by timestamp"""
        with lock.gen_rlock():
            return sorted((submissions[id] for id in submissions),
                          key=lambda sub: sub.timestamp)


with lock.gen_wlock():
    for id in listSubKeys("/submissions"):
        sub = Submission(id)
        if sub.result == Submission.RESULT_PENDING:
            sub.result = Submission.RESULT_REJECT
        submissions[id] = sub
