from django.db import models
from django.contrib.auth.models import User


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users_upvoted = models.ManyToManyField(User, related_name='upvoted_reports', blank=True)

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

class BugReport(models.Model):
    """A bug report"""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the report."""
        if len(self.text) < 50:
            return self.text
        else:
            return f"{self.text[:50]}..."