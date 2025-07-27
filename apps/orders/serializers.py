from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.serializers import ProductVariantSerializer
from apps.account.serializers import CustomerAddressSerializer




class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = CustomerAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'shipping_address', 'subtotal_amount',
            'discount_amount_saved', 'shipping_cost', 'total_amount',
            'order_status', 'payment_type', 'payment_status', 'order_date',
            'items'
        ]
