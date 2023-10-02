from django.contrib import admin
from .models import User, Address
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_superuser', 'is_seller']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'phone', 'is_default']