from django.contrib import admin

# Register your models here.

from .models import IssueType, Report

admin.site.register(IssueType)
admin.site.register(Report)