from django.db import models
from opencontest.models.problem import Problem
from opencontest.models.contest import Contest
from opencontest.models.result import Result
from opencontest.models.person import Person

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    is_full = models.BooleanField()
    contest = models.ForeignKey(Contest, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(null=False)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    code_path = models.CharField(max_length=255)
    result = models.ForeignKey(Result, on_delete=models.PROTECT)

    def __str__(self):
        return f"Submission to {self.problem} by {self.person}"
