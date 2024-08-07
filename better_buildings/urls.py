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
    path('new_report/', views.new_report, name='new_report_no_area'),
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
    # Page for viewing all reports regardless of issue area
    path('all_reports/', views.all_reports, name='all_reports'),
    # Page for editing areas
    path('edit_area/<int:area_id>/', views.edit_area, name='edit_area'),
    # Path for removing areas
    path('remove_area/<int:area_id>/', views.remove_area, name='remove_area'),
    # Page for managing areas
    path('manage_areas/', views.manage_areas, name='manage_areas'),
    # Page for managing announcements
    path('manage_announcements', views.manage_announcements, name='manage_announcements'),
    path('announcements/', views.announcements, name='announcements'),
    path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
]