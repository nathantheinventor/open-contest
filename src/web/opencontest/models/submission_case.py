from django.db import models
from opencontest.models.submission import Submission
from opencontest.models.test_case import TestCase

class SubmissionCase(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    stdout_path = models.CharField(max_length=255)
    stderr_path = models.CharField(max_length=255)

    def __str__(self):
        return f"Test case for {self.problem}"
    
    @property
    def stdout(self):
        with open(self.stdout_path) as f:
            return f.read()
    
    @property
    def stderr(self):
        with open(self.stderr_path) as f:
            return f.read()
