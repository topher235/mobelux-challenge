from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path

from .views import ProfileView


urlpatterns = [
    path('', lambda request: redirect('profile/', permanent=True)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
