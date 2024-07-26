from django.shortcuts import render, redirect

from .models import Area, Report
from .forms import AreaForm, ReportForm

# Create your views here.

def index(request):
    """The home page for Better Buildings"""
    return render(request, 'better_buildings/index.html')

def areas(request):
    """Show all issue types."""
    areas = Area.objects.order_by('date_added')
    context = {'areas': areas}
    return render(request, 'better_buildings/areas.html', context)

def area(request, area_id):
    """Show a single issue area and its reports"""
    area = Area.objects.get(id=area_id)
    reports = area.report_set.order_by('-date_added')
    context = {'area': area, 'reports': reports}
    return render(request, 'better_buildings/area.html', context)

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

def new_report(request, area_id):
    """Create a new report for a particular issue area."""
    area = Area.objects.get(id=area_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ReportForm()
    else:
        # POST data submitted; process data.
        form = ReportForm(data=request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.area = area
            new_report.save()
            return redirect('better_buildings:area', area_id=area_id)
    
    # Display a blank or invalid form.
    context = {'area': area, 'form': form}
    return render(request, 'better_buildings/new_report.html', context)

def edit_report(request, report_id):
    """Edit an existing report."""
    report = Report.objects.get(id=report_id)
    area = report.area

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = ReportForm(instance=report)
    else:
        # POST data submitted; process data.
        form = ReportForm(instance=report, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('better_buildings:area', area_id=area.id)
    
    context = {'report': report, 'area': area, 'form': form}
    return render(request, 'better_buildings/edit_report.html', context)