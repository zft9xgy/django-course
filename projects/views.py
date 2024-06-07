from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

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


def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')


    context = {
        'form': form
    }
    return render(request, 'projects/project-form.html',context)


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

def deleteProject(request,pk):
    projectObj = Project.objects.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect('projects')
        
    context = {
        'object': projectObj
    }
    return render(request, 'projects/delete-object.html',context)
