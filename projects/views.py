from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse
from .models import Project, Review
from .forms import ProjectForm, ReviewForm
from users.models import Profile
from .utils import searchProjects, paginateProjects

# Create your views here.
# Aqui controlamos toda la lógica del programa. 
# En la respuesta le mandamos el template con el contexto.


def projects(request):

    projects, searchQuery = searchProjects(request)
    projects, custom_range = paginateProjects(request,projects)

    context = {
        'projects': projects,
        'search_query':searchQuery,
        'custom_range': custom_range,
    }

    return render(request, 'projects/projects.html',context)


def project(request,pk):


    projectObj = Project.objects.get(id=pk)
    reviews = Review.objects.filter(project=projectObj)

    reviewform = ReviewForm()
    already_voters = {review.reviewer for review in reviews}

    #3 casos 
    # usuario no logueado -> mensaje para loguease
    # usuario owner del proyecto -> aviso de que no puede votar
    # usuario ya ha puesto un voto -> aviso de gracias por haber votado
    # otro caso -> formulario para el voto
    
    if request.method == 'POST':
        if (request.user.profile != projectObj.owner) and (request.user.profile != projectObj.owner):
            reviewform = ReviewForm(request.POST)
            review = reviewform.save(commit=False)
            review.reviewer = request.user.profile
            review.project = projectObj
            review.save()
            projectObj.updateVotes

            messages.success(request, 'Your review was successfully submitted!')
            return redirect('project',pk=projectObj.id)#(request.path)
            

    context = {
        'project': projectObj,
        'reviews': reviews,
        'form': reviewform,
        'already_voters': already_voters
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
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    #projectObj = Project.objects.get(id=pk)
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
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    #projectObj = Project.objects.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect('projects')
        
    context = {
        'object': projectObj
    }
    return render(request, 'delete-object.html',context)

