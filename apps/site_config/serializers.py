from rest_framework import serializers
from .models import SiteConfiguration, SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']


class SiteConfigurationSerializer(serializers.ModelSerializer):
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = SiteConfiguration
        fields = [
            'site_name', 'site_tagline', 'logo_url', 'top_bar_message',
            'default_currency', 'whatsapp_number', 'social_links'
        ]

    def get_social_links(self, obj):
        links = SocialLink.objects.all()
        return SocialLinkSerializer(links, many=True).data
