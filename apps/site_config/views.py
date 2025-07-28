from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SiteConfiguration, SocialLink
from .serializers import SiteConfigurationSerializer, SocialLinkSerializer


class SiteConfigAPIView(APIView):
    def get(self, request):
        try:
            config = SiteConfiguration.objects.first()
            if not config:
                return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Site configuration not found",
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = SiteConfigurationSerializer(config)
            return Response({
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Site configuration fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching site configuration: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocialLinksAPIView(APIView):
    def get(self, request):
        try:
            links = SocialLink.objects.all()
            serializer = SocialLinkSerializer(links, many=True)
            return Response({
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Social links fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching social links: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
