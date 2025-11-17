from django.contrib import admin
from .models import Category, Product, WishlistItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'available', 'brand', 'created_at')
    list_filter = ('available', 'category', 'brand')
    search_fields = ('name', 'sku', 'tags', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('available',)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user', 'product')





