from django.urls import path
from .views import CheckoutAPIView, OrderHistoryAPIView, OrderDetailAPIView

urlpatterns = [
    path('orders/checkout/', CheckoutAPIView.as_view(), name='order-checkout'),
    path('orders/history/', OrderHistoryAPIView.as_view(), name='order-history'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
