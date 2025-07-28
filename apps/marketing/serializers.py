from rest_framework import serializers
from apps.marketing.models import NewsletterSubscriber, FeaturedProduct
from apps.products.serializers import ProductSerializer

from rest_framework import serializers
from .models import Coupon

class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'created_at']


class FeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = FeaturedProduct
        fields = ['id', 'product', 'display_order', 'created_at']
