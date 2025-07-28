from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem._meta.get_field('product_variant').related_model.objects.all(),
        source='product_variant', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'product_variant_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at']
