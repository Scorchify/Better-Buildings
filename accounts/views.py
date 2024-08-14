from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, get_backends
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CompleteSignupForm
from django.contrib.auth.forms import AuthenticationForm
from better_buildings.models import Report
from django.conf import settings
from .models import CustomUser
from django.contrib import messages


User = get_user_model()


def is_supervisor(user):
    return user.groups.filter(name='School Supervisors').exists()

def not_authenticated(user):
    return not user.is_authenticated

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_reports_active = Report.objects.filter(owner=user, resolved=False)
    user_reports_resolved = Report.objects.filter(owner=user, resolved=True)
    context = {
        'user': user,
        'user_reports_active': user_reports_active,
        'user_reports_resolved': user_reports_resolved,
        'viewing_profile': True,
    }
    return render(request, 'accounts/user_profile.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_suspended:
                return redirect('account_suspended')
            else:
                login(request, user)
                return redirect('better_buildings:index')
        else:
            messages.error(request, 'Invalid username or password.')
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
        'viewing_profile': False,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def suspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.suspend()
    return redirect('user_profile', user_id=user_id)

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def unsuspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.unsuspend()
    return redirect('user_profile', user_id=user_id)

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

def account_suspended(request):
    return render(request, 'accounts/account_suspended.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_suspended:
                    return redirect('account_suspended')
                else:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

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
@user_passes_test(is_supervisor, login_url='/no_permission/')
def suspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_suspended:
        messages.warning(request, 'User already suspended.')
    else:
        user.suspend()
        messages.success(request, 'User suspended successfully.')
    return redirect('user_profile', user_id=user_id)

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def suspended_users(request):
    suspended_users = CustomUser.objects.filter(is_suspended=True)
    return render(request, 'accounts/suspended_users.html', {'suspended_users': suspended_users})

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def unsuspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_suspended:
        messages.warning(request, 'User is not suspended.')
    else:
        user.unsuspend()
        messages.success(request, 'User unsuspended successfully.')
    return redirect('suspended_users')

def complete_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = request.user

        if username and password:
            user.username = username
            user.set_password(password)
            user.save()

            # Re-login the user after setting the password
            login(request, user)
            return redirect('home')  # Redirect to the homepage or any other page

        else:
            # Handle the error case where username or password is missing
            return render(request, 'registration/complete_signup.html', {
                'error': 'Username and password are required.'
            })

    return render(request, 'registration/complete_signup.html')

@user_passes_test(not_authenticated, login_url='/')
def register(request):
    return render(request, 'registration/register.html')