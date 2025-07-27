from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.marketing.models import NewsletterSubscriber, FeaturedProduct
from apps.marketing.serializers import NewsletterSubscriberSerializer, FeaturedProductSerializer



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
