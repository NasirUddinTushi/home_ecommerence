from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.marketing.models import NewsletterSubscriber, FeaturedProduct
from apps.marketing.serializers import NewsletterSubscriberSerializer, FeaturedProductSerializer

from .models import Coupon, CouponUsage
from .serializers import CouponValidateSerializer
from datetime import date

class CouponValidateAPIView(APIView):
    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "code": 400,
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=400)

        code = serializer.validated_data['code']
        total = serializer.validated_data['total']
        user = request.user if request.user.is_authenticated else None

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
        except Coupon.DoesNotExist:
            return Response({
                "code": 404,
                "success": False,
                "message": "Invalid or expired coupon."
            }, status=404)

        today = date.today()
        if not (coupon.start_date <= today <= coupon.end_date):
            return Response({
                "code": 400,
                "success": False,
                "message": "Coupon not valid today."
            }, status=400)

        if total < coupon.min_order_amount:
            return Response({
                "code": 400,
                "success": False,
                "message": f"Minimum order amount is {coupon.min_order_amount}"
            }, status=400)

        if coupon.usage_limit is not None:
            used_count = CouponUsage.objects.filter(coupon=coupon).count()
            if used_count >= coupon.usage_limit:
                return Response({
                    "code": 400,
                    "success": False,
                    "message": "This coupon has reached its usage limit."
                }, status=400)

        if user and coupon.per_user_limit is not None:
            user_used = CouponUsage.objects.filter(coupon=coupon, user=user).count()
            if user_used >= coupon.per_user_limit:
                return Response({
                    "code": 400,
                    "success": False,
                    "message": "You have already used this coupon."
                }, status=400)

        # Calculate discount
        if coupon.discount_type == 'flat':
            discount = coupon.discount_value
        else:
            discount = (coupon.discount_value / 100) * total

        return Response({
            "code": 200,
            "success": True,
            "message": "Coupon applied successfully.",
            "data": {
                "discount": float(discount),
                "final_total": float(total - discount),
                "coupon_code": coupon.code
            }
        }, status=200)


class NewsletterSubscribeAPIView(APIView):
    def post(self, request):
        try:
            serializer = NewsletterSubscriberSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "code": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Subscribed to newsletter successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error subscribing to newsletter: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeaturedProductListAPIView(APIView):
    def get(self, request):
        try:
            featured_products = FeaturedProduct.objects.all().order_by('display_order')
            serializer = FeaturedProductSerializer(featured_products, many=True)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Featured products fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching featured products: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
