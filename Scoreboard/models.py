from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    score_value = models.IntegerField(default=0)
    score_date = models.DateTimeField()
    twitter_handle = models.CharField(max_length=20)
    #user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
