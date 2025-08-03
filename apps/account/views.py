from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import Customer, PasswordResetCode, CustomerAddress
from .serializers import (
    CustomerRegisterSerializer,
    CustomerSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    CustomerAddressSerializer
)
import random
import secrets


# ✅ Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "User registered successfully",
                "data": CustomerSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ✅ Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return self._handle_login(request.data)

    def get(self, request):
        email = request.query_params.get("email")
        password = request.query_params.get("password")

        if not email or not password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Email and password are required in query parameters"
            }, status=status.HTTP_400_BAD_REQUEST)

        return self._handle_login({"email": email, "password": password})

    def _handle_login(self, credentials):
        serializer = LoginSerializer(data=credentials)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Login successful",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Login failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # Get user profile
    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Profile fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # Update user profile
    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Profile update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Soft delete (deactivate account)
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Account deactivated successfully"
        }, status=status.HTTP_200_OK)


#CustomerAddress
class AddressListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = CustomerAddress.objects.filter(customer=request.user)
        serializer = CustomerAddressSerializer(addresses, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Address list fetched",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerAddressSerializer(data=request.data)
        if serializer.is_valid():
            has_address = CustomerAddress.objects.filter(customer=request.user).exists()


            serializer.save(
                customer=request.user,
                is_default=not has_address
                
                )
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Address added",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return CustomerAddress.objects.get(pk=pk, customer=user)
        except CustomerAddress.DoesNotExist:
            return None

    def put(self, request, pk):
        address = self.get_object(pk, request.user)
        if not address:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Address not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerAddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Address updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk, request.user)
        if not address:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Address not found"
            }, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Address deleted"
        }, status=status.HTTP_204_NO_CONTENT)

# Change Password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old = serializer.validated_data['old_password']
            new = serializer.validated_data['new_password']

            if not request.user.check_password(old):
                return Response({
                    "status": 400,
                    "success": False,
                    "message": "Old password is incorrect."
                }, status=400)

            request.user.set_password(new)
            request.user.save()

            return Response({
                "status": 200,
                "success": True,
                "message": "Password changed successfully."
            }, status=200)

        return Response({
            "status": 400,
            "success": False,
            "message": "Password change failed",
            "errors": serializer.errors
        }, status=400)



# Send Reset Code
class SendResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "User with this email does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        PasswordResetCode.objects.filter(email=email).delete()

        code = str(random.randint(100000, 999999))
        PasswordResetCode.objects.create(email=email, user=user, code=code)

        send_mail(
            subject="Your OTP Code",
            message=f"Your code is: {code}",
            from_email="noreply@example.com",
            recipient_list=[email]
        )

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Reset code sent to your email"
        }, status=status.HTTP_200_OK)


# Verify Reset Code
class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = Customer.objects.get(email=email)
            reset = PasswordResetCode.objects.get(user=user, code=code, is_used=False)
        except (Customer.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid or expired verification code."
            }, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_expired():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Verification code has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        reset.is_used = True
        reset.reset_token = secrets.token_hex(16)
        reset.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Verification successful.",
            "data": {
                "reset_token": reset.reset_token
            }
        }, status=status.HTTP_200_OK)


# Reset Password with Token
class ResetPasswordWithTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("reset_token")
        password = request.data.get("password")
        confirm = request.data.get("confirm_password")

        if password != confirm:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Passwords do not match."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset = PasswordResetCode.objects.get(reset_token=token, is_used=True)
        except PasswordResetCode.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid or expired reset token."
            }, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_expired():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Reset token has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = reset.user
        user.set_password(password)
        user.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Password has been reset successfully."
        }, status=status.HTTP_200_OK)


# Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Logout successful."
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid token or token already blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)
