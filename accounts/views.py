# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from better_buildings.models import Report
from django.contrib.auth import get_backends
from django.conf import settings
from .models import CustomUser

@login_required
@user_passes_test(lambda u: u.is_supervisor(), login_url='/no_permission/')
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_reports_active = Report.objects.filter(owner=user, resolved=False)
    user_reports_resolved = Report.objects.filter(owner=user, resolved=True)
    context = {
        'user': user,
        'user_reports_active': user_reports_active,
        'user_reports_resolved': user_reports_resolved,
    }
    return render(request, 'accounts/user_profile.html', context)

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
@user_passes_test(lambda u: u.is_supervisor(), login_url='/no_permission/')
def suspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.suspend()
    return redirect('user_profile', user_id=user_id)

@login_required
@user_passes_test(lambda u: u.is_supervisor(), login_url='/no_permission/')
def unsuspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.unsuspend()
    return redirect('user_profile', user_id=user_id)