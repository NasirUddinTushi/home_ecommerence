from django.contrib import admin
from .models import NewsletterSubscriber, FeaturedProduct

from django.contrib import admin
from .models import Coupon, CouponUsage
from unfold.admin import ModelAdmin

@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'start_date', 'end_date', 'active')
    search_fields = ('code',)
    list_filter = ('discount_type', 'active', 'start_date', 'end_date')


@admin.register(CouponUsage)
class CouponUsageAdmin(ModelAdmin):
    list_display = ('coupon', 'user', 'used_at')
    readonly_fields = ('coupon', 'user', 'used_at')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)


@admin.register(FeaturedProduct)
class FeaturedProductAdmin(ModelAdmin):
    list_display = ('product', 'display_order', 'created_at')
    ordering = ('display_order',)
