from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings

from apps.account.models import CustomerAddress
from apps.products.models import ProductVariant
from apps.marketing.models import Coupon, CouponUsage
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

Customer = get_user_model()


class CheckoutAPIView(APIView):
    def post(self, request):
        try:
            payload = request.data
            customer_payload = payload.get("customer_payload", {})
            shipping_info = customer_payload.get("shipping_info", {})
            summary = payload.get("summary", {})
            order_items = payload.get("order_items", [])
            frontend_payment_method = payload.get("payment_method", "Cash")

            # Extract shipping info
            email = shipping_info.get("email")
            first_name = shipping_info.get("firstName", "")
            last_name = shipping_info.get("lastName", "")
            address = shipping_info.get("address", "")
            city = shipping_info.get("city", "")
            country = shipping_info.get("country", "Bangladesh")
            postal_code = shipping_info.get("postalCode", "")

            # Map payment method
            frontend_payment_method = payload.get("payment_method", "Cash")
            payment_type = frontend_payment_method.strip().upper()

            # Validate payment method
            valid_methods = ['CASH', 'BKASH', 'NAGAD', 'ROCKET']
            if payment_type not in valid_methods:
                return Response({
                    "code": 400,
                    "success": False,
                    "message": f"Invalid payment method: {payment_type}"
                }, status=400)

            # Handle customer (guest or authenticated)
            if request.user.is_authenticated:
                customer = request.user
            else:
                if not email:
                    return Response({"code": 400, "success": False, "message": "Email is required for guest checkout"}, status=400)
                customer, _ = Customer.objects.get_or_create(
                    email=email,
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "is_guest": True
                    }
                )

            # Create shipping address
            shipping_address = CustomerAddress.objects.create(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
                phone="",
                address=address,
                city=city,
                postal_code=postal_code,
                country=country
            )

            # Summary values
            subtotal = Decimal(str(summary.get("subtotal", "0")))
            delivery = Decimal(str(summary.get("delivery", "0")))
            discount = Decimal(str(summary.get("discount_amount", "0")))
            total = Decimal(str(summary.get("total", subtotal + delivery - discount)))
            coupon_code = summary.get("discount_code")

            # Create order
            order = Order.objects.create(
                customer=customer,
                shipping_address=shipping_address,
                payment_type=payment_type,
                payment_status="pending",
                subtotal_amount=subtotal,
                shipping_cost=delivery,
                discount_amount=discount,
                total_amount=total
            )

            # Coupon logic
            coupon = None
            if coupon_code:
                try:
                    today = timezone.now().date()
                    coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)

                    if not (coupon.start_date <= today <= coupon.end_date):
                        raise Exception("Coupon not valid today.")

                    if coupon.usage_limit and CouponUsage.objects.filter(coupon=coupon).count() >= coupon.usage_limit:
                        raise Exception("Coupon usage limit reached.")

                    if coupon.per_user_limit and CouponUsage.objects.filter(coupon=coupon, user=customer).count() >= coupon.per_user_limit:
                        raise Exception("You have already used this coupon.")

                    if subtotal < coupon.min_order_amount:
                        raise Exception(f"Minimum order amount is {coupon.min_order_amount}")

                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=customer if not customer.is_guest else None
                    )

                    order.coupon = coupon
                    order.save()

                except Exception as e:
                    order.delete()
                    return Response({"code": 400, "success": False, "message": f"Coupon error: {str(e)}"}, status=400)

            # Add order items
            for item in order_items:
                product_id = item.get("product_id")
                quantity = item.get("quantity", 1)
                attributes = item.get("attributes", {})

                variant = ProductVariant.objects.filter(product_id=product_id).first()
                if not variant:
                    return Response({
                        "code": 400,
                        "success": False,
                        "message": f"No variant found for product_id={product_id}"
                    }, status=400)

                unit_price = variant.price_override or variant.product.price

                OrderItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=quantity,
                    unit_price=unit_price,
                    attributes=attributes  # Store selected attributes
                )

            # Send order confirmation email
            try:
                send_mail(
                    subject="Order Confirmation",
                    message=f"Hi {first_name},\n\nYour order #{order.id} has been placed successfully. We’ll notify you once it’s on the way.\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True
                )
            except Exception as email_err:
                print(f"Email sending failed: {email_err}")

            return Response({
                "code": 201,
                "success": True,
                "message": "Order placed successfully",
                "data": OrderSerializer(order).data
            }, status=201)

        except Exception as e:
            return Response({
                "code": 500,
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }, status=500)


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
