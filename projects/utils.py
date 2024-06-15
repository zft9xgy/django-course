from django.db.models import Q
from .models import Project, Tag

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

    return projects,searchQuery