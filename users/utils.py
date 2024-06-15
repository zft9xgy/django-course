from django.db.models import Q
from .models import Profile, Skill



def searchProfiles(request):

    if request.method == 'GET':
        searchQuery = request.GET.get('search_query') or ""

    if searchQuery:
        print(searchQuery)
        skills = Skill.objects.filter(name__icontains=searchQuery)
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=searchQuery) | 
            Q(short_intro__icontains=searchQuery) |
            Q(skill__in=skills)
            )
    else:
        profiles = Profile.objects.all()

    return profiles,searchQuery