from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.account.models import CustomerAddress
from apps.products.models import ProductVariant
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
            shipping_address = CustomerAddress.objects.create(
                customer=customer,
                full_name=data.get('name'),
                phone=data.get('phone'),
                address_line1=data.get('address_line1'),
                address_line2=data.get('address_line2', ''),
                city=data.get('city'),
                state=data.get('state', ''),
                zip_code=data.get('zip_code'),
                country=data.get('country', 'Bangladesh')
            )

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

            order.subtotal_amount = subtotal
            order.total_amount = subtotal + order.shipping_cost
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
