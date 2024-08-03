from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Report
from .models import Area, Report
from .forms import AreaForm, ReportForm


# Custom functions
def is_supervisor(user):
    return user.groups.filter(name='School Supervisors').exists()

def is_student(user):
    return user.groups.filter(name='Students').exists()

# Views

def index(request):
    """The home page for Better Buildings"""
    return render(request, 'better_buildings/index.html')

def areas(request):
    """Show all issue types."""
    areas = Area.objects.order_by('date_added')
    supervisor = request.user.groups.filter(name='School Supervisors').exists()
    context = {'areas': areas, 'supervisor': supervisor}
    return render(request, 'better_buildings/areas.html', context)

@login_required
def area(request, area_id):
    """Show a single issue area and its reports"""
    area = Area.objects.get(id=area_id)
    reports = area.report_set.order_by('-date_added')
    user_reports = area.report_set.filter(owner=request.user).order_by('-date_added')

    context = {'area': area, 'reports': reports, 'user_reports': user_reports}
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
            return redirect('better_buildings:areas')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'better_buildings/new_area.html', context)

@login_required
def new_report(request, area_id):
    """Create a new report for a particular issue area."""
    
    """    
    try to set the area to the submitted area, or if first
    generating the page, set it to the area of the area page
    previously on.
    """ 
    try:
        area = request.area
    except AttributeError:
        area = Area.objects.get(id=area_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ReportForm(initial={'area': area})
    else:
        # POST data submitted; process data.
        form = ReportForm(data=request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.area = area
            new_report.owner = request.user
            new_report.save()
            return redirect('better_buildings:area', area_id=area_id)
    
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

def upvote_report(request, report_id):
    if request.method == 'POST':
        try:
            report = Report.objects.get(id=report_id)
            report.upvotes += 1
            report.save()
            return JsonResponse({'upvotes': report.upvotes})
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)