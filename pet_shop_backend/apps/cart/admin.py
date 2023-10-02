from django.contrib import admin
from .models import Cart
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'product_id', 'number', 'is_checked']