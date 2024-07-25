from django.shortcuts import render

from .models import Area, Report

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