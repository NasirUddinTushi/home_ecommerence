from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.models import ProductVariant
from apps.marketing.models import Coupon
from apps.account.serializers import CustomerAddressSerializer, CustomerSerializer


# Product variant display serializer (readonly)
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'price_override']


# Order Item Serializer (readonly)
class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_variant', 'quantity', 'unit_price']


# Coupon Serializer (readonly)
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value']


# Read-only Order Serializer for display
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    shipping_address = CustomerAddressSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    subtotal_amount = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    shipping_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'shipping_address',
            'coupon',
            'discount_amount',
            'subtotal_amount',
            'shipping_cost',
            'total_amount',
            'payment_type',
            'payment_status',
            'status',
            'items',
            'total_quantity',
            'created_at'
        ]

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_subtotal_amount(self, obj):
        return str(obj.subtotal_amount)

    def get_total_amount(self, obj):
        return str(obj.total_amount)

    def get_discount_amount(self, obj):
        return str(obj.discount_amount)

    def get_shipping_cost(self, obj):
        return str(obj.shipping_cost)


# Inline serializer for address during checkout
class CustomerAddressInlineSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)


# Input serializer for checkout
class OrderCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    payment_type = serializers.ChoiceField(choices=['COD', 'ONLINE'])
    address = CustomerAddressInlineSerializer(required=False)
    address_id = serializers.IntegerField(required=False)
    items = serializers.ListSerializer(
        child=serializers.DictField(), allow_empty=False
    )
    coupon_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
