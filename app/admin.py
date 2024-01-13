from django.contrib import admin

# Register your models here.
from .models import User, CustomerProfile, DeliveryPersonProfile, Order, OrderItem, OrderHistory

# admin.site.register(User)
admin.site.register(DeliveryPersonProfile)
admin.site.register(CustomerProfile)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'tracking_number', 'status')
    
@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
    
@admin.register(OrderHistory)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'timestamp', 'tracking_number')
    