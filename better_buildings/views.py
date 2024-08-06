from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from .models import Report
from .models import Area, Report, BugReport
from .forms import AreaForm, ReportForm, BugReportForm
from django.shortcuts import get_object_or_404
from .models import Announcement
from .forms import AnnouncementForm

# Custom functions
def is_supervisor(user):
    return user.groups.filter(name='School Supervisors').exists()

def is_student(user):
    return user.groups.filter(name='Students').exists()

def is_admin(user):
    return user.is_superuser

# Views

def index(request):
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.is_superuser
    areas = Area.objects.all()  # Fetch all areas here
    context = {
        'is_admin': is_admin,
        'areas': areas
    }
    return render(request, 'better_buildings/index.html', context)

@login_required
def area(request, area_id):
    """Show a single issue area and its reports"""
    area = Area.objects.get(id=area_id)
    reports = area.report_set.filter(resolved=False).order_by('-upvotes', '-date_added')
    user_reports = area.report_set.filter(owner=request.user, resolved=False).order_by('-upvotes', '-date_added')
    resolved_reports = area.report_set.filter(resolved=True).order_by('-resolved_date')
    user = request.user
    is_supervisor = user.groups.filter(name="School Supervisors").exists()

    if request.method == 'POST' and 'resolve' in request.POST:
        report_id = request.POST.get('report_id')
        report = Report.objects.get(id=report_id)
        report.resolve_issue()
        report.set_resolved_date()
        report.save()
        return redirect('better_buildings:area', area_id=area_id)

    context = {
        'area': area,
        'reports': reports,
        'user_reports': user_reports,
        'resolved_reports': resolved_reports,
        'is_supervisor': is_supervisor
    }
    return render(request, 'better_buildings/area.html', context)

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
def new_area(request):
    """Add a new issue area."""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = AreaForm()
    else:
        # POST data submitted; process data.
        form = AreaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('better_buildings:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'better_buildings/new_area.html', context)

@login_required
def new_report(request, area_id=None):
    """Create a new report for a particular issue area."""
    
    if area_id:
        try:
            area = Area.objects.get(id=area_id)
        except Area.DoesNotExist:
            return redirect('better_buildings:index')
    else:
        area = None

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ReportForm()
    else:
        # POST data submitted; process data.
        form = ReportForm(data=request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.area = form.cleaned_data['area']  # Get the selected area from the form
            new_report.owner = request.user
            new_report.save()
            if area:
                return redirect('better_buildings:area', area_id=area.id)
            else:
                # Redirect to the display page of the newly created report’s area
                return redirect('better_buildings:area', area_id=new_report.area.id)

    # Display a blank or invalid form.
    context = {'area': area, 'form': form}
    return render(request, 'better_buildings/new_report.html', context)



@login_required
def edit_report(request, report_id):
    """Edit an existing report."""
    report = Report.objects.get(id=report_id)
    
    area = report.area

    if report.owner != request.user:
        return redirect('better_buildings:no_permission')

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = ReportForm(instance=report, initial={'area': area})
    else:
        # POST data submitted; process data.
        form = ReportForm(instance=report, data=request.POST)
        if 'delete' in request.POST:
            report.delete()
            return redirect('better_buildings:area', area_id=area.id)
        else:
            if form.is_valid():
                form.save()
                return redirect('better_buildings:area', area_id=area.id)

    context = {'report': report, 'area': area, 'form': form}
    return render(request, 'better_buildings/edit_report.html', context)

def no_permission(request):
    """Page to be displayed when a user doesn't have acess to a page"""
    return render(request, 'better_buildings/no_permission.html')

def upvote_report(request, report_id): #upvoting
    if request.method == 'POST':
        try:
            report = Report.objects.get(id=report_id)
            if request.user.is_authenticated:
                user = request.user
                report.toggle_upvote(user)
                return JsonResponse({'upvotes': report.upvotes, 'has_upvoted': report.users_upvoted.filter(id=user.id).exists()})
            else:
                return JsonResponse({'error': 'User not authenticated'}, status=403)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def report_bug(request):
    """Page to report a website bug"""
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BugReportForm()
    else:
        # POST data submitted; process data.
        form = BugReportForm(data=request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.owner = request.user
            new_report.save()
            return redirect('better_buildings:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'better_buildings/report_bug.html', context)

@login_required
@user_passes_test(is_admin, login_url='/no_permission/')
def view_bug_reports(request):
    """Page for admin account to view bug reports"""
    if 'delete' in request.POST:
        report_id = request.POST.get('report_id')
        bug_report = BugReport.objects.get(id=report_id)
        bug_report.delete()
        return redirect('better_buildings:view_bug_reports')

    reports = BugReport.objects.order_by('date_added')
    context = {'reports': reports}
    return render(request, 'better_buildings/view_bug_reports.html', context)

@login_required
def all_reports(request):
    """Page for viewing all reports regardless of issue area"""
    reports = Report.objects.all()
    norm_reports = reports.filter(resolved=False).order_by('-upvotes', '-date_added')
    user_reports = reports.filter(owner=request.user, resolved=False).order_by('-upvotes', '-date_added')
    resolved_reports = reports.filter(resolved=True).order_by('-resolved_date')
    is_supervisor = request.user.groups.filter(name="School Supervisors").exists()

    if request.method == 'POST' and 'resolve' in request.POST:
        report_id = request.POST.get('report_id')
        report = Report.objects.get(id=report_id)
        report.resolve_issue()
        report.set_resolved_date()
        report.save()
        return redirect('better_buildings:all_reports')

    context = {
        'norm_reports': norm_reports,
        'user_reports': user_reports,
        'resolved_reports': resolved_reports,
        'is_supervisor': is_supervisor
    }
    return render(request, 'better_buildings/all_reports.html', context)

def edit_area(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('better_buildings:manage_areas')
    else:
        form = AreaForm(instance=area)
    return render(request, 'better_buildings/edit_area.html', {'form': form})

@require_http_methods(["DELETE"])
def remove_area(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    area.delete()
    return JsonResponse({'success': True})

@login_required
@user_passes_test(is_admin, login_url='/no_permission/')
def manage_areas(request):
    areas = Area.objects.all()  # Fetch areas from the database
    return render(request, 'better_buildings/manage_areas.html', {'areas': areas})

@login_required
def announcements(request):
    announcements = Announcement.objects.all()
    is_supervisor = request.user.groups.filter(name='Supervisors').exists()
    return render(request, 'better_buildings/announcements.html', {'announcements': announcements, 'is_supervisor': is_supervisor})

@login_required
@user_passes_test(is_admin, login_url='/no_permission/')
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('better_buildings:announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'better_buildings/create_announcement.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/no_permission/')
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('better_buildings:announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'better_buildings/edit_announcement.html', {'form': form, 'announcement_id': announcement_id})