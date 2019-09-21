from django.http import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json
import urllib.request
from .forms import HomeForm
import git
import os
import shutil
from .models import GitUserDetail, RepositoryDetails, GitFiles, Context
import sqlite3


def get_repos(request):
    form = HomeForm()
    template_name = 'GitUserTemplate/UserForm.html'
    # when user input is received
    if request.method == 'POST':
        template_name = 'GitUserTemplate/FilesList.html'
        username = request.POST.get("GitUserName")
        # connect to DB
        con = sqlite3.connect('db.sqlite3')
        cursorObj = con.cursor()
        # check if username already exists in DB
        cursorObj.execute('SELECT * FROM gitUserRepos_gituserdetail WHERE username=?', (username,))
        userdata = cursorObj.fetchall()
        # If the username already exist in DB, fetch the details.
        if userdata:
            context = fetchData(username, cursorObj, userdata)
        # If the username is not found in the DB, add to DB and display the results
        else:
            context = saveData(username)
        return render(request, template_name, context)
    else:
        # Render empty form if it is a GET request
        form = HomeForm()
    return render(request, template_name, {'form': form})


def fetchData(username, cursorObj, userdata):
    for row in userdata:
        cursorObj.execute('SELECT * FROM gitUserRepos_repositorydetails WHERE username_id=?', (row[0],))
        repositorydata = cursorObj.fetchall()
        if repositorydata:
            for row in repositorydata:
                Context.repo_count = Context.repo_count + 1
                cursorObj.execute('SELECT * FROM gitUserRepos_gitfiles WHERE repository_details_id=?', (row[0],))
                filesdata = cursorObj.fetchall()
                if filesdata:
                    # for key, value in filesdata:
                    for file_row in filesdata:
                        # Decode the json string
                        json_files = json.loads(file_row[2])
                        # iterate over file(s) from json object. Ex : ["py", "manage"]
                        for file in json_files[1]:
                            Context.files_dict.setdefault(json_files[0], [])
                            Context.files_dict[json_files[0]].append(file)
                    # Add the list of file belonging to this repository
                    Context.list_repos[row[1]] = Context.files_dict
    context = {'username': username, 'Context': Context}
    return context


def saveData(username):
    url = 'https://api.github.com/users/' + username + '/repos'
    data = urllib.request.urlopen(url)
    item_dict = json.loads(data.read())
    root_dir = 'E:\Shravya\Python Projects\Temporary'
    # count of number of repositories
    repo_count = 0
    # list of repo urls
    list_repos = {}
    # dictionary to store files of each repository
    files_dict = {}
    # list to store all files belonging to all respositories (list of dictionary items)
    list_files = []
    # store user details to DB
    user = GitUserDetail(username=username)
    user.save()
    for item in item_dict:
        repo_count = repo_count + 1
        repositoryurl = item.get('html_url')
        # store Repository Urls to DB
        repo_url = RepositoryDetails(repository_url=repositoryurl, username=user)
        repo_url.save()
        # clone the repository url and save in local temp folder
        git.Git(root_dir).clone(repositoryurl)
        # dirName: Directory Path;
        # subdirList: A list of sub-directories in the current directory;
        # fileList: A list of files in the current sub-directory.
        for dirName, subdirList, fileList in os.walk(root_dir):
            if '.git' in dirName:
                continue
            for filename in fileList:
                filename = filename.split(".")
                # key : file extension
                key = str(filename[len(filename) - 1])
                if (key == ('gitignore' or 'gitignore~')) or (str(filename[0]) == "") is True:
                    continue
                files_dict.setdefault(key, [])
                files_dict[key].append(str(filename[0]))
        list_repos[repositoryurl] = files_dict
        for key, value in files_dict.items():
            # store files, belonging to this repository, to DB
            file = GitFiles(file=(key, value), repository_details=repo_url)
            file.save()
    shutil.rmtree(root_dir, ignore_errors=True, onerror=None)
    context = {'username': username, 'repo_count': repo_count, 'repo_url': list_repos, 'file_dict': files_dict}
    return  context







