from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, get_backends
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from .forms import CustomAuthenticationForm, CustomSocialSignupForm
from django.contrib.auth.forms import AuthenticationForm
from better_buildings.models import Report
from django.conf import settings
from .models import CustomUser
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount

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
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'registration/login.html', context)

@login_required
def profile(request):
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
    if request.method == 'POST':
        form = CustomSocialSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.username = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            # If user signed up with Google, link social account
            social_account = SocialAccount.objects.filter(user=user, provider='google').first()
            if social_account:
                user.email = social_account.extra_data['email']
                user.save()

            login(request, user)
            return redirect('index')
    else:
        form = CustomSocialSignupForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def account_suspended(request):
    return render(request, 'accounts/account_suspended.html')

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def suspended_users(request):
    suspended_users = CustomUser.objects.filter(is_suspended=True)
    context = {'suspended_users': suspended_users}
    return render(request, 'accounts/suspended_users.html', context)