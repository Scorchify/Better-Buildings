from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from better_buildings.models import Report
from django.contrib.auth.decorators import login_required

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display a blank form
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('better_buildings:index')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    """Allow a user to view account information"""
    user_reports = Report.objects.filter(owner=request.user)
    user = request.user
    context = {
        'user_reports': user_reports,
        'username': user.username,
    }
    return render(request, 'accounts/profile.html', context)