from django.contrib.auth.models import AbstractUser
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_suspended = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

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
