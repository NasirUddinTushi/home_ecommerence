from django.contrib import admin
from .models import NewsletterSubscriber, FeaturedProduct


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)


@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_order', 'created_at')
    ordering = ('display_order',)
