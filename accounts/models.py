from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_suspended = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    def suspend(self):
        self.is_suspended = True
        self.is_active = False
        self.save()

    def unsuspend(self):
        self.is_suspended = False
        self.is_active = True
        self.save()
    
    def is_supervisor(self):
        return self.groups.filter(name='Supervisor').exists()
