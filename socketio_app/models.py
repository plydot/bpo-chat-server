from django.db import models


class UserRoom(models.Model):
    sid = models.CharField(max_length=100)
    username = models.CharField(max_length=25)
