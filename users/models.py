# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='attendee', null=True)
    attendee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
