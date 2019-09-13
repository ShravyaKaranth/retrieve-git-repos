from django.http import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json
import urllib.request
from .forms import HomeForm


def get_repos(request):
    form = HomeForm()
    template_name = 'GitUser/UserForm.html'
    # count of number of repositories
    count = 0
    # when user input is received
    if request.method == 'POST':
        name = request.POST.get("GitUserName")
        url = 'https://api.github.com/users/'+name+'/repos'
        data = urllib.request.urlopen(url)
        item_dict = json.loads(data.read())
        for item in item_dict:
            if item.get('id') is None:
                continue
            count = count + 1
        return HttpResponse('The count of repositories created by ' + name + ' is ' + str(count))
    else:
        # Render empty form if it is a GET request
        form = HomeForm()
    return render(request, template_name, {'form': form})







