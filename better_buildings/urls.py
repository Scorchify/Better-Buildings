"""Defines URL patterns for better_buildings."""

from django.urls import path

from . import views

app_name = 'better_buildings'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that displays the reports relating to an issue area
    path('area/<int:area_id>/', views.area, name='area'),
    # Page for adding a new issue area.
    path('new_area/', views.new_area, name='new_area'),
    # Page for creating a new report.
    path('new_report/<int:area_id>/', views.new_report, name='new_report'),
    # Page for editing an entry
    path('edit_report/<int:report_id>/', views.edit_report, name='edit_report'),
    # Redirect page for when a user attempts to access a page they don't have access to
    path('no_permission/', views.no_permission, name='no_permission'),
    # Handles Upvoting Logic
    path('upvote/<int:report_id>/', views.upvote_report, name='upvote_report'),
    # Page for reporting a website bug or suggestion
    path('report_bug/', views.report_bug, name='report_bug'),
    # Page for admin account to view bug reports
    path('view_bug_reports/', views.view_bug_reports, name='view_bug_reports'),
]