from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.serializers import ProductVariantSerializer
from apps.marketing.models import Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_variant', 'quantity', 'unit_price']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'shipping_address', 'coupon', 'discount_amount',
            'subtotal_amount', 'shipping_cost', 'total_amount',
            'payment_type', 'payment_status', 'status', 'items', 'created_at'
        ]
