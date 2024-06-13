from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.userAccount, name="account"),
    path('edit-profile/', views.updateProfile, name="edit-profile"),
]
