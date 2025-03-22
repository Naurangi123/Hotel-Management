from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default_image.jpg', null=True, blank=True)
    is_customer = models.BooleanField(default=True)
    is_hotel_owner = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)