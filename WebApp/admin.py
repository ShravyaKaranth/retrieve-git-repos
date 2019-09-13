from django.contrib import admin
from .models import GitUserDetail


class GitUser(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(GitUserDetail, GitUser)

