from django.db import models

class Contest(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    scoreboard_freeze = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
