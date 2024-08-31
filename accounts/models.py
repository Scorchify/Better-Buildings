from django.contrib.auth.models import AbstractUser
from django.db import models
from better_buildings.models import School  # Import the School model from better_buildings

class CustomUser(AbstractUser):
    is_suspended = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    student_school = models.ForeignKey(School, related_name='students', on_delete=models.SET_NULL, null=True, blank=True)  

    def suspend(self):
        self.is_suspended = True
        self.is_active = False
        self.save()

    def unsuspend(self):
        self.is_suspended = False
        self.is_active = True
        self.save()

    def is_supervisor(user):
        return user.groups.filter(name='School Supervisors').exists()