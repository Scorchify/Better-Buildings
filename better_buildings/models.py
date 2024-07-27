from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Area(models.Model):
    """A report of a building issue."""
    text = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Report(models.Model):
    """A building issue report linked to an issue type"""
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    upvotes = 0
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a simple string representing the report."""
        return f"{self.text[:50]}..."

    def upvote(self):
        upvotes += 1