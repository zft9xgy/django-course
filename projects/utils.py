from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):

    if request.method == 'GET':
        searchQuery = request.GET.get('search_query') or ""

    if searchQuery:
        tags = Tag.objects.filter(name__icontains=searchQuery)

        projects = Project.objects.distinct().filter(
            Q(title__icontains=searchQuery) | 
            Q(description__icontains=searchQuery) |
            Q(owner__name__icontains=searchQuery) |
            Q(tags__in=tags)
            )
    else:
        projects = Project.objects.all()

    return projects, searchQuery
    


def paginateProjects(request,projects):

    items_per_page = 3
    pagination_half_range = 2
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

    return projects, custom_range