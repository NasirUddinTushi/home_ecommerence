from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView, CustomerAddressAPIView

urlpatterns = [
    path('account/register/', RegisterAPIView.as_view(), name='customer-register'),
    path('account/login/', LoginAPIView.as_view(), name='customer-login'),
    path('account/profile/', ProfileAPIView.as_view(), name='customer-profile'),
    path('account/addresses/', CustomerAddressAPIView.as_view(), name='customer-addresses'),
]
