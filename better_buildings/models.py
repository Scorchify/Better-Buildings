from django.db import models
from django.utils import timezone
from django.conf import settings  # Import settings to use AUTH_USER_MODEL


# Create your models here.

class Area(models.Model):
    """An area a issue is reported in"""
    text = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Report(models.Model):
    """A building issue report linked to an issue area"""
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users_upvoted = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_reports', blank=True)
    resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return a simple string representing the report."""
        if len(self.text) < 50:
            return self.text
        else:
            return f"{self.text[:50]}..."

    def toggle_upvote(self, user):
        if self.users_upvoted.filter(id=user.id).exists():
            self.upvotes -= 1
            self.users_upvoted.remove(user)
        else:
            self.upvotes += 1
            self.users_upvoted.add(user)
        self.save()
    
    def resolve_issue(self):
        self.resolved = True
    
    def set_resolved_date(self):
        self.resolved_date = timezone.now()

class BugReport(models.Model):
    """A bug report"""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the report."""
        if len(self.text) < 50:
            return self.text
        else:
            return f"{self.text[:50]}..."

class Announcement(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)  # Defaulted to False
    resolved_date = models.DateTimeField(null=True, blank=True)  # New field

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