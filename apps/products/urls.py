from django.urls import path
from .views import (
    ProductListAPIView, ProductDetailAPIView,
    FeaturedProductListAPIView, CategoryListAPIView, CategoryDetailAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/featured/', FeaturedProductListAPIView.as_view(), name='product-featured'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),
]
