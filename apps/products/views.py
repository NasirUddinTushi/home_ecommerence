from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer, RecursiveCategorySerializer


class ProductListAPIView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all().order_by('-created_at')
            serializer = ProductSerializer(products, many=True)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Product list fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching products: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
            serializer = ProductSerializer(product)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Product detail fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching product: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeaturedProductListAPIView(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(is_featured=True)
            serializer = ProductSerializer(products, many=True)
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

class CategoryListAPIView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.filter(parent__isnull=True).order_by('name')  # Only top-level
            serializer = RecursiveCategorySerializer(categories, many=True)
            return Response({
                "code": 200,
                "success": True,
                "message": "Category list fetched successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "code": 500,
                "success": False,
                "message": f"Error fetching categories: {str(e)}"
            }, status=500)



class CategoryDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            serializer = CategorySerializer(category)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Category detail fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching category: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
