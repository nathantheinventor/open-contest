from django.db import models
from opencontest.models.problem import Problem

class TestCase(models.Model):
    class Meta:
        ordering = ['order']

    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    input_path = models.CharField(max_length=255)
    output_path = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f"Test case for {self.problem}"
    
    @property
    def input(self):
        with open(self.input_path) as f:
            return f.read()
    
    @property
    def output(self):
        with open(self.output_path) as f:
            return f.read()
