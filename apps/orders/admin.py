from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_status', 'payment_type', 'total_amount', 'created_at')
    list_filter = ('order_status', 'payment_type', 'payment_status')
    search_fields = ('customer__email', 'customer__first_name', 'customer__last_name')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
