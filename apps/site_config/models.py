from django.db import models

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default="Forestland Linen")
    site_tagline = models.CharField(max_length=255, blank=True)
    logo_url = models.ImageField(upload_to="site/logo/", blank=True, null=True)
    top_bar_message = models.CharField(max_length=255, blank=True)
    default_currency = models.CharField(max_length=10, default="BDT")
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.platform
