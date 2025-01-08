from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('technician', 'Technician')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_approved = models.BooleanField(default=False)

class TechnicianRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.TextField()
    qualifications = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
