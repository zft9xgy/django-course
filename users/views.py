from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all()

    context = {'profiles':profiles}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profileObj = Profile.objects.get(id=pk)

    topSkills = profileObj.skill_set.exclude(description__exact="")
    otherSkills = profileObj.skill_set.filter(description="")

    context = {'profile':profileObj,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        # se comprueba que el usuario existe y si existe lo devuelve
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # A backend authenticated the credentials
            login(request, user) 
            messages.success(request, 'User login correctly.')
            nextUrl = request.GET.get("next", "/")
            return redirect(nextUrl)
        else:
            # No backend authenticated the credentials
            messages.error(request, 'User or password wrong!')
        
    return render(request,'users/login-register.html')



def logoutUser(request):
    messages.success(request, 'User logout correctly. Good bye.')
    logout(request)
    return redirect('/')
