from django.db import models
from stats.models import User, Theme, Participation

# Create your models here.
class UserResult(models.Model):
    user = models.ForeignKey('stats.User')
    theme = models.ForeignKey('stats.Theme')
    participation = models.ForeignKey('stats.Participation', null=True)
    solved = models.IntegerField()