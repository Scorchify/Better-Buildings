# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('better_buildings:index')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def custom_login(request):
    """Custom login view."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('better_buildings:index')
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'registration/login.html', context)

@login_required
def profile(request):
    """User profile view."""
    return render(request, 'registration/profile.html')

@login_required
def suspend_user(request, user_id):
    """Suspend a user."""
    user = CustomUser.objects.get(id=user_id)
    user.suspend()
    return redirect('accounts:profile')

@login_required
def unsuspend_user(request, user_id):
    """Unsuspend a user."""
    user = CustomUser.objects.get(id=user_id)
    user.unsuspend()
    return redirect('accounts:profile')