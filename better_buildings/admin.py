from django.contrib import admin

# Register your models here.

from .models import Area, Report

admin.site.register(Area)
admin.site.register(Report)