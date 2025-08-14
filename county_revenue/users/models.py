from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    NATIONAL_ID = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    ROLE_CHOICES = [('citizen','Citizen'),('staff','Staff'),('admin','Admin')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    def __str__(self):
        return f"{self.username} ({self.role})"