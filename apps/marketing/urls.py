from django.urls import path
from .views import NewsletterSubscribeAPIView, FeaturedProductListAPIView, CouponValidateAPIView

urlpatterns = [
    path('marketing/newsletter/', NewsletterSubscribeAPIView.as_view(), name='newsletter-subscribe'),
    path('marketing/featured/', FeaturedProductListAPIView.as_view(), name='featured-products'),
    path('coupons/validate/', CouponValidateAPIView.as_view(), name='validate-coupon'),
]
