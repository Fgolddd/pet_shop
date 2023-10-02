from django.contrib import admin
from .models import Category, Product, Detail, Banner, Collect

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'is_on']

@admin.register(Banner)
class ProductBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']

@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'vender']