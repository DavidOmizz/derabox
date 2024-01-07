from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

status = (
    (0,'inactive'),
    (1,'active'),
)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('delivery', 'Delivery'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Add other common fields like name, address, etc.

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='customer-profile-pictures')
    address = models.CharField(max_length= 255, blank=True, null = True)
    # Add customer-specific fields
    
    def __str__(self):
        return self.user.username

class DeliveryPersonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='customer-profile-pictures')
    address = models.CharField(max_length= 255, blank=True, null = True)
    status = models.IntegerField(choices = status, default= 0)
    # Add delivery personnel-specific fields
    
    def __str__(self):
        return self.user.username

# Additional models can be added as needed.