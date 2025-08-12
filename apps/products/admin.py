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



@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(AttributeValue)
class AttributeValueAdmin(ModelAdmin):
    list_display = ("attribute", "value")
    search_fields = ("value", "attribute__name")
    list_filter = ("attribute",)
    ordering = ("attribute", "value")
    list_select_related = ("attribute",)  # perf


@admin.register(ProductVariantValue)
class ProductVariantValueAdmin(ModelAdmin):
    list_display = ("variant", "attribute_value")
    search_fields = ("variant__sku", "attribute_value__value", "attribute_value__attribute__name")
    list_filter = ("attribute_value__attribute", "variant__product")
    ordering = ("variant",)
    list_select_related = ("variant", "attribute_value")  # perf