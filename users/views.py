from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCustomRegisterForm, ProfileForm

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
    page = 'login'
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

    context = {
        'page': page
    }
        
    return render(request,'users/login-register.html',context)

def logoutUser(request):
    messages.success(request, 'User logout correctly. Good bye.')
    logout(request)
    return redirect('/')

#crear views
#crear url
# modificar plantilla para enlazar
# ok
# crear form para registro 
# capturarlo en vista
# validarlo 
# crear usuario

def registerUser(request):
    
    if request.method == 'POST':
        form = UserCustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'Registration was success!')
            
            login(request, user)
            return redirect('account')
        else:
            messages.error(request,'A problem as occurred un registration')
    else:
        form = UserCustomRegisterForm()



    context = {
        'page': 'register',
        'form': form,
    }
        
    return render(request,'users/login-register.html',context)



@login_required(login_url='login')
def userAccount(request):
    profile = Profile.objects.get(user=request.user)
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
            'profile': profile,
            'skills': skills,
            'projects': projects,
        }
    return render(request, 'users/user-account.html',context)


@login_required(login_url='login')
def updateProfile(request):
    
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ProfileForm(instance=profile)


    context = {
        'form': form,
        }
    return render(request, 'users/edit-profile.html',context)

#ok update profile 
#ok crear views.py y funcion
#ok añadir a url.py
# crear form.py
# añadir a la plantilla
# crear signals para que cuando se modifique el profile se modifique user
# en username, first_name y email profile - User
