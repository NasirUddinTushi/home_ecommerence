from django.urls import path
from .views import SiteConfigAPIView, SocialLinksAPIView

urlpatterns = [
    path('site-config/', SiteConfigAPIView.as_view(), name='site-config'),
    path('social-links/', SocialLinksAPIView.as_view(), name='social-links'),
]
