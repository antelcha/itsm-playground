from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserModel(models.Model):

    ROLE_CHOICES = [
          ('user', 'End User'),
          ('agent', 'IT Agent'),
          ('admin', 'Administrator'),
      ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    employee_id = models.CharField(max_length=255)
    

    def __str__(self):
          return f"{self.user.username} - {self.get_role_display()}"