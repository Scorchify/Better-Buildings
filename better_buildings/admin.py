from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.

from .models import Area, Report, BugReport,School 

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'ip_address')
    search_fields = ('name', 'domain', 'ip_address')

admin.site.register(School, SchoolAdmin)

admin.site.register(Area)
admin.site.register(Report)
admin.site.register(Permission)
admin.site.register(BugReport)