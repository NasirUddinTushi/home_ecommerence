from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    SendResetCodeView,
    VerifyResetCodeView,
    ResetPasswordWithTokenView,
    LogoutView,
    AddressListCreateAPIView,
    AddressDetailAPIView
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Password Reset via Email
    path('forgot-password/send-code/', SendResetCodeView.as_view(), name='send-reset-code'),
    path('forgot-password/verify-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('forgot-password/reset/', ResetPasswordWithTokenView.as_view(), name='reset-password'),

    # Customer Address CRUD
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
]
