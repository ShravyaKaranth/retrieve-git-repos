from django.db import models
import jsonfield


class GitUserDetail(models.Model):
    username = models.CharField(max_length=255, unique=True)


class RepositoryDetails(models.Model):
    repository_url = models.CharField(max_length=255)
    username = models.ForeignKey(GitUserDetail, on_delete=models.CASCADE)


class GitFiles(models.Model):
    file = jsonfield.JSONField()
    repository_details = models.ForeignKey(RepositoryDetails, on_delete=models.CASCADE)


class Context(models.Model):
    repo_count = 0
    list_repos = {}
    files_dict = {}

