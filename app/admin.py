from django.contrib import admin

# Register your models here.
from .models import User, CustomerProfile, DeliveryPersonProfile

# admin.site.register(User)
admin.site.register(DeliveryPersonProfile)
admin.site.register(CustomerProfile)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type',)
    