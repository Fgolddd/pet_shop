from django.contrib import admin
from .models import Order, OrderProducts, Comment
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'amount', 'status', 'order_code']

@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'product']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','order', 'user', 'product']

