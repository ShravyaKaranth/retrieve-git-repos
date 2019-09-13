from django.db import models


class GitUserDetail(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=100)

