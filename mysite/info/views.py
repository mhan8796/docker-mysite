from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

from .forms import CfSpaceForm
from .forms import BbProjectForm
from .forms import JrProjectForm
from . import conf_methods
from . import bb_methods
from . import jr_methods


def get_confluence_space_admin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CfSpaceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            space_index = form.cleaned_data['space_index']
            if not str.isdigit(space_index):
                # try space name
                ret = conf_methods.query_name(space_index)
                if ret:
                    # give the admin names
                    admins = conf_methods.throw_admin(ret[0][0])
                    return render(request, 'info/list-cf-space-admins.html',{'admins': admins})
                else:
                    # try space key
                    ret = conf_methods.query_key(space_index)
                    if ret:
                        # give the admin names
                        admins = conf_methods.throw_admin(ret[0][0])
                        return render(request, 'info/list-cf-space-admins.html',{'admins': admins})
                return render(request, 'info/cf-space-not-found.html')
            else:
            	# try space id
                ret = conf_methods.query_id(space_index)
                if ret:
                    # give the admin names
                    admins = conf_methods.throw_admin(ret[0][0])
                    return render(request, 'info/list-cf-space-admins.html',{'admins': admins})
                return render(request, 'info/cf-space-not-found.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CfSpaceForm()
    return render(request, 'info/cf-admin.html', {'form': form})


def get_bb_project_admin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BbProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project_key = form.cleaned_data['project_key']

            ret = bb_methods.query_key(project_key)
            if ret:
                admins = bb_methods.throw_admin(ret[0][0])
                return render(request, 'info/list-bb-project-admins.html', {'admins': admins})
            else:
                return render(request, 'info/bb-project-not-found.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BbProjectForm()
    return render(request, 'info/bb-admin.html', {'form': form})


def get_jr_project_admin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JrProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project_key = form.cleaned_data['project_key']
            ret = jr_methods.query_key(project_key)
            if ret:
                admins = jr_methods.throw_admin(ret[0][0],project_key)
                return render(request, 'info/list-jr-project-admins.html', {'admins': admins})
            else:
                return render(request, 'info/jr-project-not-found.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = JrProjectForm()
    return render(request, 'info/jr-admin.html', {'form': form})


def index(request):
    return render(request, 'info/info.html')
    # return HttpResponse("Hello, world. You're at the polls index.")