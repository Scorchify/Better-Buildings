# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from better_buildings.models import Report
from django.contrib.auth import get_backends
from django.conf import settings

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            backend = settings.AUTHENTICATION_BACKENDS[0]  # Get the first backend path
            login(request, new_user, backend=backend)
            return redirect('better_buildings:index')
    else:
        form = CustomUserCreationForm()
    
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
    """Allow a user to view account information"""
    user_reports_active = Report.objects.filter(owner=request.user, resolved=False)
    user_reports_resolved = Report.objects.filter(owner=request.user, resolved=True)
    user = request.user
    context = {
        'user_reports_active': user_reports_active,
        'user_reports_resolved': user_reports_resolved,
        'username': user.username,
    }
    return render(request, 'accounts/profile.html', context)


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