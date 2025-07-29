from django.urls import path
from .views import (
RegisterAPIView, LoginAPIView, ProfileAPIView, CustomerAddressAPIView,
LogoutView, SendResetCodeView, VerifyResetCodeView, ResetPasswordWithTokenView)

urlpatterns = [
    path('account/register/', RegisterAPIView.as_view(), name='customer-register'),
    path('account/login/', LoginAPIView.as_view(), name='customer-login'),
    path('account/profile/', ProfileAPIView.as_view(), name='customer-profile'),
    path('account/addresses/', CustomerAddressAPIView.as_view(), name='customer-addresses'),


    # Password Reset URLs
    path("password-reset/send-code/", SendResetCodeView.as_view(), name="send_reset_code"),
    path("password-reset/verify-code/", VerifyResetCodeView.as_view(), name="verify_reset_code"),
    path("password-reset/reset-with-token/", ResetPasswordWithTokenView.as_view(), name="reset_password_with_token"),

    # Logout
    path("logout/", LogoutView.as_view(), name="logout"),
]
