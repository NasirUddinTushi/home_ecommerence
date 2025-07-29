from django.contrib import admin
from .models import Order, OrderItem
from unfold.admin import ModelAdmin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_variant', 'quantity', 'unit_price')


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'payment_type', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_type', 'payment_status')
    search_fields = ('customer__email', 'shipping_address__full_name')
    inlines = [OrderItemInline]
    readonly_fields = ('subtotal_amount', 'discount_amount', 'total_amount', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('customer', 'shipping_address', 'coupon', 'discount_amount')
        }),
        ('Payment Info', {
            'fields': ('payment_type', 'payment_status')
        }),
        ('Order Totals', {
            'fields': ('subtotal_amount', 'shipping_cost', 'total_amount')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )
