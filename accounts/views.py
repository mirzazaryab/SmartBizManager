# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:overview')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:overview')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:overview')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Do NOT log the user in
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # Redirect to login page
    return render(request, 'accounts/register.html')

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('profile')  # update this name to match your profile view

    return render(request, 'accounts/profile.html', {'profile': profile})

def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})