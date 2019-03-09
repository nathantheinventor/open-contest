from django.db import models
from opencontest.models.contest import Contest

class Problem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    statement = models.CharField(max_length=1000)
    input_format = models.CharField(max_length=1000)
    output_format = models.CharField(max_length=1000)
    constraints = models.CharField(max_length=1000)
    sample_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
