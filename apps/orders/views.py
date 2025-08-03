from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from apps.account.models import CustomerAddress
from apps.products.models import ProductVariant
from apps.marketing.models import Coupon, CouponUsage
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

Customer = get_user_model()


class CheckoutAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "code": 400,
                "success": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=400)

        data = serializer.validated_data
        customer = request.user if request.user.is_authenticated else None

        # Guest user logic
        if not customer:
            email = data.get("email")
            if not email:
                return Response({"code": 400, "success": False, "message": "Email is required for guest checkout"}, status=400)

            customer, _ = Customer.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": data.get("name", ""),
                    "phone": data.get("phone", ""),
                    "is_guest": True
                }
            )

        # Address creation
        if "address_id" in data:
            try:
                shipping_address = CustomerAddress.objects.get(id=data["address_id"], customer=customer)
            except CustomerAddress.DoesNotExist:
                return Response({"code": 404, "success": False, "message": "Address not found"}, status=404)
        elif "address" in data:
            addr = data["address"]
            shipping_address = CustomerAddress.objects.create(
                customer=customer,
                first_name=addr["first_name"],
                last_name=addr["last_name"],
                phone=addr["phone"],
                address=addr["address"],
                city=addr["city"],
                postal_code=addr["postal_code"],
                country=addr.get("country", "Bangladesh")
            )
        else:
            return Response({"code": 400, "success": False, "message": "Shipping address required"}, status=400)

        # Order & Items
        subtotal = Decimal('0.00')
        order = Order.objects.create(
            customer=customer,
            shipping_address=shipping_address,
            subtotal_amount=Decimal('0.00'),
            shipping_cost=Decimal('0.00'),
            discount_amount=Decimal('0.00'),
            total_amount=Decimal('0.00'),
            payment_type=data["payment_type"],
            payment_status="pending"
        )

        for item in data.get('items', []):
            variant_id = item.get("variant_id")
            product_id = item.get("product_id")

            if variant_id:
                variant = ProductVariant.objects.get(id=variant_id)
            elif product_id:
                variant = ProductVariant.objects.filter(product_id=product_id).first()
                if not variant:
                    return Response({
                        "code": 400,
                        "success": False,
                        "message": f"No variant found for product_id={product_id}"
                    }, status=400)
            else:
                return Response({
                    "code": 400,
                    "success": False,
                    "message": "Each item must have either variant_id or product_id"
                }, status=400)

            quantity = item.get('quantity', 1)
            unit_price = variant.price_override or variant.product.price
            subtotal += unit_price * quantity

            OrderItem.objects.create(
                order=order,
                product_variant=variant,
                quantity=quantity,
                unit_price=unit_price
            )

        # Coupon logic
        discount = Decimal('0.00')
        coupon_code = data.get("coupon_code")
        coupon = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                today = timezone.now().date()

                if not (coupon.start_date <= today <= coupon.end_date):
                    raise Exception("Coupon not valid today.")

                if coupon.usage_limit and CouponUsage.objects.filter(coupon=coupon).count() >= coupon.usage_limit:
                    raise Exception("Coupon usage limit reached.")

                if coupon.per_user_limit and CouponUsage.objects.filter(coupon=coupon, user=customer).count() >= coupon.per_user_limit:
                    raise Exception("You have already used this coupon.")

                if subtotal < coupon.min_order_amount:
                    raise Exception(f"Minimum order amount is {coupon.min_order_amount}")

                discount = (
                    coupon.discount_value if coupon.discount_type == 'flat'
                    else (coupon.discount_value / Decimal('100.0')) * subtotal
                )

                CouponUsage.objects.create(
                    coupon=coupon,
                    user=customer if not customer.is_guest else None
                )

            except Exception as e:
                order.delete()
                return Response({"code": 400, "success": False, "message": f"Coupon error: {str(e)}"}, status=400)

        # Final totals
        order.subtotal_amount = subtotal
        order.discount_amount = discount
        order.total_amount = subtotal - discount + order.shipping_cost
        order.coupon = coupon if coupon else None
        order.save()

        return Response({
            "code": 201,
            "success": True,
            "message": "Order placed successfully",
            "data": OrderSerializer(order).data
        }, status=201)


class OrderHistoryAPIView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(customer=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response({
                "code": 200,
                "success": True,
                "message": "Order history fetched successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "code": 500,
                "success": False,
                "message": f"Error fetching orders: {str(e)}"
            }, status=500)


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            serializer = OrderSerializer(order)
            return Response({
                "code": 200,
                "success": True,
                "message": "Order detail fetched successfully",
                "data": serializer.data
            }, status=200)
        except Order.DoesNotExist:
            return Response({
                "code": 404,
                "success": False,
                "message": "Order not found"
            }, status=404)
        except Exception as e:
            return Response({
                "code": 500,
                "success": False,
                "message": f"Error fetching order: {str(e)}"
            }, status=500)
