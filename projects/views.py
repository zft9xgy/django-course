from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from users.models import Profile

# Create your views here.
# Aqui controlamos toda la lógica del programa. 
# En la respuesta le mandamos el template con el contexto.


def projects(request):
    projects = Project.objects.all()
    
    context = {
        'projects': projects
    }
    return render(request, 'projects/projects.html',context)


def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    context = {
        'project': projectObj
    }
    return render(request, 'projects/single-project.html',context)


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            project.owner = profile
            project.save()
            return redirect('projects')


    context = {
        'form': form
    }
    return render(request, 'projects/project-form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('projects')


    context = {
        'form': form
    }
    return render(request, 'projects/project-form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    projectObj = Project.objects.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect('projects')
        
    context = {
        'object': projectObj
    }
    return render(request, 'projects/delete-object.html',context)
