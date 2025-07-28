from django.urls import path
from .views import CartView, AddToCartAPIView, RemoveFromCartAPIView, UpdateCartItemAPIView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
]
