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



# Order item serializer (readonly)

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_variant', 'quantity', 'unit_price', 'attributes']  # ✅ attributes added



# Coupon serializer (readonly)

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value']



# Order serializer (readonly)

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



# Inline serializer for address (optional use)

class CustomerAddressInlineSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)


# Input serializer for Checkout Payload


class ShippingInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    postalCode = serializers.CharField()
    paymentMethod = serializers.ChoiceField(choices=['Cash', 'Bkash', 'Nagad', 'Rocket'])


class CustomerPayloadSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(allow_null=True)
    shipping_info = ShippingInfoSerializer()


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    attributes = serializers.DictField(
        child=serializers.IntegerField(), required=False
    )


class SummarySerializer(serializers.Serializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateSerializer(serializers.Serializer):
    customer_payload = CustomerPayloadSerializer()
    payment_method = serializers.ChoiceField(choices=['Cash', 'Bkash', 'Nagad', 'Rocket'])
    order_items = OrderItemInputSerializer(many=True)
    summary = SummarySerializer()
