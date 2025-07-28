from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.products.models import ProductVariant


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response({
            "code": 200,
            "success": True,
            "message": "Cart fetched successfully",
            "data": serializer.data
        })


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            variant_id = request.data.get("product_variant_id")
            quantity = int(request.data.get("quantity", 1))

            if not variant_id:
                return Response({
                    "code": 400,
                    "success": False,
                    "message": "Product variant ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            variant = ProductVariant.objects.get(id=variant_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()

            return Response({
                "code": 201,
                "success": True,
                "message": "Item added to cart successfully",
                "data": CartItemSerializer(item).data
            }, status=status.HTTP_201_CREATED)
        except ProductVariant.DoesNotExist:
            return Response({
                "code": 400,
                "success": False,
                "message": "Invalid product variant ID"
            }, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return Response({
                "code": 200,
                "success": True,
                "message": "Item removed from cart"
            })
        except CartItem.DoesNotExist:
            return Response({
                "code": 404,
                "success": False,
                "message": "Cart item not found"
            }, status=status.HTTP_404_NOT_FOUND)


class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            quantity = int(request.data.get("quantity", item.quantity))
            item.quantity = quantity
            item.save()
            return Response({
                "code": 200,
                "success": True,
                "message": "Cart item updated",
                "data": CartItemSerializer(item).data
            })
        except CartItem.DoesNotExist:
            return Response({
                "code": 404,
                "success": False,
                "message": "Cart item not found"
            }, status=status.HTTP_404_NOT_FOUND)
