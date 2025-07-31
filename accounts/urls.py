# accounts/urls.py
from django.urls import path
from . import views

namespace = 'accounts'

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),  # Optional, for /accounts/login/
]