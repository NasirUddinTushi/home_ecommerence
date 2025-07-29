from django.contrib import admin
from .models import Cart, CartItem
from unfold.admin import ModelAdmin


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('id', 'cart', 'product_variant', 'quantity')
    list_filter = ('cart', 'product_variant')
    search_fields = ('cart__user__email', 'product_variant__product__name')
