from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)  # store website
    ip_address = models.CharField(max_length=45, unique=True, required=False)  # IPv4 and IPv6
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        default_areas = [
            'Bathrooms',
            'Hallways',
            'Classrooms',
            'Cafeteria',
        ]
        if is_new:
            for area_name in default_areas:
                Area.objects.create(text=area_name, school=self)
    
class Area(models.Model):
    text = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.text

class Report(models.Model):
    area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(null=True, blank=True)
    upvoted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_reports', blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    def toggle_upvote(self, user):
        if user in self.upvoted_by.all():
            self.upvotes -= 1
            self.upvoted_by.remove(user)
        else:
            self.upvotes += 1
            self.upvoted_by.add(user)
        self.save()

    def __str__(self):
        return self.text if len(self.text) < 50 else f"{self.text[:50]}..."

    def resolve_issue(self):
        self.resolved = True
        self.set_resolved_date()

    def set_resolved_date(self):
        self.resolved_date = timezone.now()

class BugReport(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.text if len(self.text) < 50 else f"{self.text[:50]}..."

class Announcement(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(null=True, blank=True)
    seen_by = models.ManyToManyField(get_user_model(), related_name='seen_announcements', blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if self.resolved and not self.resolved_date:
            self.resolved_date = timezone.now()
        elif not self.resolved:
            self.resolved_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        if self.resolved:
            return f"{self.text} (Resolved on {self.resolved_date})"
        return self.text