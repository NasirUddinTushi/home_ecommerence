from django.contrib import admin
from .models import SiteConfiguration, SocialLink


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_tagline', 'whatsapp_number', 'updated_at')
    search_fields = ('site_name', 'site_tagline')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')
    search_fields = ('platform',)
