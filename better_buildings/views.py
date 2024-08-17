from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.contrib import messages
from .resources.blacklist import blacklist
from .models import Area, Report, BugReport, Announcement
from .forms import AreaForm, ReportForm, BugReportForm, AnnouncementForm
from difflib import SequenceMatcher
import json
import re

#dictionary
ordinal_map = {
    'first': '1',
    'second': '2',
    'third': '3',
    'fourth': '4',
    'fifth': '5',
    'sixth': '6',
    'seventh': '7',
    'eighth': '8',
    'ninth': '9',
    'tenth': '10'
    # Add more as needed
}

# Custom functions
def is_supervisor(user):
    return user.groups.filter(name='School Supervisors').exists()

def is_student(user):
    return user.groups.filter(name='Students').exists()

def is_admin(user):
    return user.is_superuser

def extract_numbers(text):
    return re.findall(r'\d+', text)

def convert_ordinals(text):
    for word, number in ordinal_map.items():
        text = re.sub(r'\b' + word + r'\b', number, text)
    return text

def is_similar(text1, text2, threshold=0.6):
    # Convert text to lowercase
    text1 = text1.lower()
    text2 = text2.lower()
    
    # Convert ordinal words to numbers
    text1 = convert_ordinals(text1)
    text2 = convert_ordinals(text2)
    
    # Extract numbers
    numbers1 = extract_numbers(text1)
    numbers2 = extract_numbers(text2)
    
    # Remove numbers from the text
    text1_without_numbers = re.sub(r'\d+', '', text1)
    text2_without_numbers = re.sub(r'\d+', '', text2)
    
    # Compare text similarity without numbers
    text_similarity = SequenceMatcher(None, text1_without_numbers, text2_without_numbers).ratio()
    
    # Compare numbers (if any)
    numbers_match = numbers1 == numbers2
    
    # Consider the reports similar only if both text similarity and numbers match
    return text_similarity > threshold and numbers_match

def check_blacklist(text):
    for word in blacklist:
        if word in text:
            return True
    return False


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
    """Show a single issue area and its reports."""
    area = get_object_or_404(Area, id=area_id)
    reports = area.report_set.filter(resolved=False).order_by('-upvotes', '-date_added')
    user_reports = area.report_set.filter(owner=request.user, resolved=False).order_by('-upvotes', '-date_added')
    resolved_reports = area.report_set.filter(resolved=True).order_by('-resolved_date')
    user = request.user
    is_supervisor = user.groups.filter(name="School Supervisors").exists()

    # Dictionary to check if the current user has upvoted each report
    upvoted_reports = {report.id: report.upvoted_by.filter(id=user.id).exists() for report in reports}

    if request.method == 'POST' and 'resolve' in request.POST:
        report_id = request.POST.get('report_id')
        report = get_object_or_404(Report, id=report_id)
        report.resolve_issue()
        report.set_resolved_date()
        report.save()
        return redirect('better_buildings:area', area_id=area_id)

    context = {
        'area': area,
        'reports': reports,
        'user_reports': user_reports,
        'resolved_reports': resolved_reports,
        'is_supervisor': is_supervisor,
        'upvoted_reports': upvoted_reports
    }
    return render(request, 'better_buildings/area.html', context)

@login_required
@require_POST
def upvote_report(request, report_id):
    """Toggle the upvote status of a report."""
    report = get_object_or_404(Report, id=report_id)
    user = request.user
    
    if report.upvoted_by.filter(id=user.id).exists():
        report.upvoted_by.remove(user)
        report.upvotes -= 1
    else:
        report.upvoted_by.add(user)
        report.upvotes += 1
    
    report.save()
    return JsonResponse({'upvotes': report.upvotes})

@login_required
def report_state(request, report_id):
    """Provide the upvote state of a report."""
    report = get_object_or_404(Report, id=report_id)
    is_upvoted = report.upvoted_by.filter(id=request.user.id).exists()
    return JsonResponse({'is_upvoted': is_upvoted})

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
            new_area = form.save()
            return redirect('better_buildings:area', area_id=new_area.id)
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'better_buildings/new_area.html', context)

@login_required
def new_report(request, area_id=None):
    """Create a new report for a particular issue area."""
    area = None
    if area_id:
        area = get_object_or_404(Area, id=area_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ReportForm(initial={'area': area} if area else None)
    else:
        form = ReportForm(data=request.POST)
        if form.is_valid():
            new_report_text = form.cleaned_data['text']
            if check_blacklist(new_report_text):
                form.add_error('text', 'Your report contains inappropriate language. Please revise and resubmit.')
            else:
                if area:
                    similar_report = None
                    for report in area.report_set.all():
                        if is_similar(new_report_text, report.text):
                            similar_report = report
                            break
                    if similar_report:
                        messages.warning(request, f'A similar report already exists: "{similar_report.text}"')
                    else:
                        new_report = form.save(commit=False)
                        new_report.area = form.cleaned_data['area']
                        new_report.owner = request.user
                        new_report.save()
                        return redirect('better_buildings:area', area_id=area.id)
                else:
                    # If area is None, set the area based on form input
                    new_report = form.save(commit=False)
                    new_report.owner = request.user
                    new_report.save()
                    return redirect('better_buildings:area', area_id=new_report.area.id)

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
        if 'delete' in request.POST:
            area.delete()
            return redirect('better_buildings:manage_areas')
        else:
            form = AreaForm(request.POST, instance=area)
            if form.is_valid():
                form.save()
                return redirect('better_buildings:manage_areas')
    else:
        form = AreaForm(instance=area)
    return render(request, 'better_buildings/edit_area.html', {'form': form, 'area': area})

@login_required
@user_passes_test(is_supervisor, login_url='/no_permission/')
@require_POST
def delete_report(request, report_id):
    """Delete a report."""
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect(request.META.get('HTTP_REFERER', 'better_buildings:index'))

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
    unresolved_announcements = Announcement.objects.filter(resolved=False)
    resolved_announcements = Announcement.objects.filter(resolved=True)
    context = {
        'announcements': unresolved_announcements,
        'resolved_announcements': resolved_announcements,
    }
    return render(request, 'better_buildings/announcements.html', context)

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
            return redirect('better_buildings:manage_announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'better_buildings/edit_announcement.html', {'form': form, 'announcement': announcement})

@login_required
@user_passes_test(is_admin, login_url='/no_permission/')
def manage_announcements(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        announcement_id = data.get('announcement_id')
        action = data.get('action')

        try:
            announcement = Announcement.objects.get(id=announcement_id)
            if action == 'delete':
                announcement.delete()
                return JsonResponse({'success': True})
            elif action == 'resolve':
                announcement.resolved = True
                announcement.save()
                return JsonResponse({'success': True})
        except Announcement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Announcement not found'})

    unresolved_announcements = Announcement.objects.filter(resolved=False)
    resolved_announcements = Announcement.objects.filter(resolved=True)
    context = {
        'announcements': unresolved_announcements,
        'resolved_announcements': resolved_announcements,
        'is_supervisor': is_supervisor(request.user)
    }
    return render(request, 'better_buildings/manage_announcements.html', context)