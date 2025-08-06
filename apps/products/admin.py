from django.contrib import admin
from .models import Product, Category, ProductImage, ProductVariant, Attribute, AttributeValue, ProductVariantValue
from unfold.admin import ModelAdmin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)



admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductVariantValue)
