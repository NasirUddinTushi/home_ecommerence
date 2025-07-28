from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from apps.account.models import CustomerAddress
from apps.products.models import ProductVariant
from apps.marketing.models import Coupon, CouponUsage
from .models import Order, OrderItem
from .serializers import OrderSerializer

Customer = get_user_model()


class CheckoutAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            customer = request.user if request.user.is_authenticated else None

            # Guest user creation
            if not customer:
                guest_email = data.get('email')
                if not guest_email:
                    return Response({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "message": "Email is required for guest checkout"
                    }, status=status.HTTP_400_BAD_REQUEST)

                customer = Customer.objects.create(
                    email=guest_email,
                    first_name=data.get('name', ''),
                    phone=data.get('phone', ''),
                    is_guest=True
                )

            # Create shipping address
            shipping_address = None
            if "address_id" in data:
                try:
                    shipping_address = CustomerAddress.objects.get(id=data["address_id"], customer=customer)
                except CustomerAddress.DoesNotExist:
                    return Response({
                        "code": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Address not found"
                    }, status=status.HTTP_404_NOT_FOUND)
            elif "address" in data:
                addr = data["address"]
                shipping_address = CustomerAddress.objects.create(
                    customer=customer,
                    full_name=addr.get("full_name"),
                    phone=addr.get("phone"),
                    address_line1=addr.get("address_line1"),
                    address_line2=addr.get("address_line2", ""),
                    city=addr.get("city"),
                    state=addr.get("state", ""),
                    zip_code=addr.get("zip_code"),
                    country=addr.get("country", "Bangladesh")
                )
            else:
                return Response({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "Either address_id or address details must be provided"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create Order
            subtotal = 0
            order = Order.objects.create(
                customer=customer,
                shipping_address=shipping_address,
                subtotal_amount=0,
                total_amount=0,
                payment_type="COD",
                payment_status="pending"
            )

            for item in data.get('items', []):
                variant_id = item.get('variant_id')
                quantity = item.get('quantity', 1)
                variant = ProductVariant.objects.get(id=variant_id)
                unit_price = variant.price_override or variant.product.price
                subtotal += unit_price * quantity
                OrderItem.objects.create(order=order, product_variant=variant, quantity=quantity, unit_price=unit_price)

            discount = 0
            coupon = None
            coupon_code = data.get("coupon_code")
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                    today = date.today()

                    if not (coupon.start_date <= today <= coupon.end_date):
                        raise ValueError("Coupon not valid today.")

                    if coupon.usage_limit is not None:
                        used_count = CouponUsage.objects.filter(coupon=coupon).count()
                        if used_count >= coupon.usage_limit:
                            raise ValueError("This coupon has reached its usage limit.")

                    if customer and coupon.per_user_limit is not None:
                        user_used = CouponUsage.objects.filter(coupon=coupon, user=customer).count()
                        if user_used >= coupon.per_user_limit:
                            raise ValueError("You have already used this coupon.")

                    if subtotal < coupon.min_order_amount:
                        raise ValueError(f"Minimum order amount is {coupon.min_order_amount}")

                    discount = (
                        coupon.discount_value if coupon.discount_type == 'flat'
                        else (coupon.discount_value / 100) * subtotal
                    )

                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=customer if customer.is_authenticated else None
                    )
                except Exception as e:
                    return Response({
                        "code": 400,
                        "success": False,
                        "message": f"Coupon error: {str(e)}"
                    }, status=400)

            order.subtotal_amount = subtotal
            order.discount_amount = discount
            order.total_amount = subtotal - discount + order.shipping_cost
            if coupon:
                order.coupon = coupon
            order.save()

            response = {
                "code": status.HTTP_201_CREATED,
                "success": True,
                "message": "Order placed successfully",
                "data": OrderSerializer(order).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except ProductVariant.DoesNotExist:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid product variant ID",
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error creating order: {str(e)}",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderHistoryAPIView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(customer=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Order history fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching orders: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            serializer = OrderSerializer(order)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Order detail fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching order: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
