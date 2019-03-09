from django.db import models
from django.utils import timezone

class Contest(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    scoreboard_freeze = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name

    @staticmethod
    def current():
        for contest in Contest.objects.all():
            if contest.start <= timezone.now() <= contest.end:
                return contest
        return None
