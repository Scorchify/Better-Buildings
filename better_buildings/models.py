from django.db import models

# Create your models here.

class IssueType(models.Model):
    """A report of a building issue."""
    text = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Report(models.Model):
    """A building issue report linked to an issue type"""
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a simple string representing the entry."""
        return f"{self.text[:50]}..."