from django.contrib import admin
from .models import SiteConfiguration, SocialLink
from unfold.admin import ModelAdmin

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(ModelAdmin):
    list_display = [
        'site_name',
        'site_tagline',
        'default_currency',
        'whatsapp_number',
        'instagram_handle',
        'updated_at'
    ]
    search_fields = ['site_name', 'whatsapp_number']
    list_filter = ['default_currency', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ['platform', 'url']
    search_fields = ['platform']
