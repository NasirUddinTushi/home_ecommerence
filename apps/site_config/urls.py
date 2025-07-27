from django.urls import path
from .views import SiteConfigurationAPIView

urlpatterns = [
    path('site-config/', SiteConfigurationAPIView.as_view(), name='site-config'),
]
