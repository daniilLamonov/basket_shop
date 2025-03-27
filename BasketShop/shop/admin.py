from django.contrib import admin

from .models import Product, Category, Brand, ProductImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
class ProductImageInline(admin.TabularInline):  # или admin.StackedInline
    model = ProductImage
    extra = 1  # Количество пустых полей для загрузки новых фото
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'available']
    list_filter = ['category', 'price', 'available']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]