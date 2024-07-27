from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.

from .models import Area, Report

admin.site.register(Area)
admin.site.register(Report)
admin.site.register(Permission)