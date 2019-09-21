from django.contrib import admin
from .models import GitUserDetail, RepositoryDetails, GitFiles


# Register your models here.
class GitUser(admin.ModelAdmin):
    list_display = ('username',)


class RepoDetails(admin.ModelAdmin):
    list_display = ('repository_url', 'username')


class Files(admin.ModelAdmin):
    list_display = ('file', 'repository_details')


admin.site.register(GitUserDetail, GitUser)
admin.site.register(RepositoryDetails, RepoDetails)
admin.site.register(GitFiles, Files)
