from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'category', 'brand')
    search_fields = ('name', 'sku', 'tags')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WishlistItem)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','product','added_at')

