from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    def save(self):
        if self.password is None:
            self.password = "test"
        if self.user is None:
            self.user = User.objects.create_user(self.user, 'none@none', self.password)
            self.user.save()
        super().save()
