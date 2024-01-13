from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='customersprofile')
    profile_picture = models.ImageField(upload_to='customer-profile-pictures')
    address = models.CharField(max_length= 255, blank=True, null = True)
    # Add customer-specific fields
    
    def __str__(self):
        return self.user.username

class DeliveryPersonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='deliveryprofile')
    profile_picture = models.ImageField(upload_to='delivery-profile-pictures')
    address = models.CharField(max_length= 255, blank=True, null = True)
    status = models.IntegerField(choices = status, default= 0)
    # Add delivery personnel-specific fields
    
    def __str__(self):
        return self.user.username

# Additional models can be added as needed.



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=15, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default = 'Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # previous_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], null=True, blank=True) This wa for privious signals.

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            # Generate the tracking number when saving for the first time
            current_year = timezone.now().year
            last_order = Order.objects.filter(tracking_number__startswith=f'TK{current_year}').order_by('-tracking_number').first()

            if last_order:
                last_tracking_number = int(last_order.tracking_number[10:])
                new_tracking_number = f'TK{current_year}{str(last_tracking_number + 1).zfill(5)}'
            else:
                new_tracking_number = f'TK{current_year}00001'

            self.tracking_number = new_tracking_number

        super().save(*args, **kwargs)
        
        # if self.pk is not None:
        #     original = Order.objects.get(pk=self.pk)
        #     if original.status != self.status:
        #         self.previous_status = original.status
        # super(Order, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.user.username


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tracking_number = models.CharField(max_length=20, unique=True)
#     status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
    
#     def __str__(self) -> str:
#         return self.user.username
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return self.product_name
    
class OrderHistory(models.Model):
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    timestamp = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=15, unique=True, editable=False)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.order.user.username



#Signals ---------------------------- 
# @receiver(post_save, sender=Order)
# def create_order_history(sender, instance, created, **kwargs):
#     if not created and instance.status != instance.previous_status:
#         OrderHistory.objects.create(order=instance, status=instance.status)


# @receiver(post_save, sender=Order)
# def create_order_history(sender, instance, created, **kwargs):
#     if not created and instance.status != instance.previous_status:
#         # Check if an entry with the same status already exists
#         existing_history = OrderHistory.objects.filter(order=instance, status=instance.status).first()

#         if not existing_history:
#             OrderHistory.objects.create(order=instance, status=instance.status)


# @receiver(pre_save, sender=Order)
# def create_order_history(sender, instance, **kwargs):
#     try:
#         original = Order.objects.get(pk=instance.pk)
#     except Order.DoesNotExist:
#         # For new orders
#         original = None

#     if original and original.status != instance.status:
#         # Check if an entry with the same status already exists
#         existing_history = OrderHistory.objects.filter(order=instance, status=instance.status).first()

#         if not existing_history:
#             OrderHistory.objects.create(order=instance, status=instance.status)

# @receiver(post_save, sender=Order)
# def create_order_history(sender, instance, created, **kwargs):
#     if created:
#         OrderHistory.objects.create(order=instance, status=instance.status)

@receiver(post_save, sender=Order)
def update_order_history(sender, instance, **kwargs):
    try:
        # Try to get the corresponding OrderHistory
        order_history = OrderHistory.objects.get(order=instance)
        # Update the status
        order_history.status = instance.status
        order_history.tracking_number = instance.tracking_number
        order_history.save()
    except OrderHistory.DoesNotExist:
        # If no OrderHistory exists, create one
        OrderHistory.objects.create(order=instance, status=instance.status, tracking_number=instance.tracking_number)
        
        
