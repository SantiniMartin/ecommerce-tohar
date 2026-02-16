from django.contrib import admin

from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'discount_percentage')
    list_filter = ('category',)
    search_fields = ('name', 'description')

