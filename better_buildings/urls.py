"""Defines URL patterns for better_buildings."""

from django.urls import path

from . import views

app_name = 'better_buildings'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that displays issue areas
    path('areas/', views.areas, name='areas'),
    # Page that displays the reports relating to an issue area
    path('area/<int:area_id>/', views.area, name='area'),
]