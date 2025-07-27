from django.urls import path
from .views import NewsletterSubscribeAPIView, FeaturedProductListAPIView

urlpatterns = [
    path('marketing/newsletter/', NewsletterSubscribeAPIView.as_view(), name='newsletter-subscribe'),
    path('marketing/featured/', FeaturedProductListAPIView.as_view(), name='featured-products'),
]
