from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete





# User es el modelo por defecto de django que tine dependencias con autenticación y demás
# por eso usamos un modelo Profile, para evitar tocar y modificar User.
# Profile toma datos user, como 'username' 'email' 'first_name'
# Cuando se crear un modelo User, se debe crear un modelo Profile y enlazarlos
# Cuando se crear un Profile, se debe crear un User y enlazarlos
# Cuando User se borra, Profile se borra
# Cuando Porifle se borra, User de borra
# Cuando User se modifica, Profile se modifica
# Cuando Profile se modifica, User se modifica?



def createProfile(sender,instance,created,**kwargs):
    # create a profile when user is create and connect.
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name = user.first_name,
            username = user.username,
            email = user.email,
        )

def deleteUser(sender,instance,**kwargs):
    #delete user when profile is delete.
    profile = instance
    user = profile.user
    user.delete()
    

def updateProfile(sender,instance,created,**kwargs):
# Cuando se actualia un perfil, se debe actualizar el first_name, username e email del User.abs
    if not created:
        profile = instance
        user = profile.user
        user.username = profile.username
        user.email = profile.email
        user.first_name = profile.name
        user.save()


# cuando se crear un User se debe crear un Profile y asignarlo
post_save.connect(createProfile,sender=User)
post_save.connect(updateProfile,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)
