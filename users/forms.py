from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Skill



class UserCustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(UserCustomRegisterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website']

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)

        #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Okay title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name','description']

    def __init__(self,*args,**kwargs):
        super(SkillForm,self).__init__(*args,**kwargs)

        #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Okay title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})