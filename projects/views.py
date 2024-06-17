from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from users.models import Profile
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
# Aqui controlamos toda la lógica del programa. 
# En la respuesta le mandamos el template con el contexto.


def projects(request):

    items_per_page = 3
    pagination_half_range = 2

    projects, searchQuery = searchProjects(request)
    page_numer = request.GET.get('page')

    
    paginator = Paginator(projects,items_per_page)

    try:
        projects = paginator.page(page_numer)
    except PageNotAnInteger:
        page_numer = 1
        projects = paginator.page(page_numer)
    except EmptyPage:
        page_numer = paginator.num_pages
        projects = paginator.page(page_numer)

    
    total_page_number = paginator.num_pages 
    actual_page_number = projects.number 

    leftIndex = actual_page_number - pagination_half_range 

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = actual_page_number + pagination_half_range + 1 

    if rightIndex > total_page_number:
        rightIndex = total_page_number + 1
 
    custom_range = range(leftIndex,rightIndex)
    
   
    context = {
        'projects': projects,
        'search_query':searchQuery,
        'custom_range': custom_range,
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

