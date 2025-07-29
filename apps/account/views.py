from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.account.models import CustomerAddress,  Customer
from apps.account.serializers import CustomerSerializer, CustomerRegisterSerializer, CustomerAddressSerializer, LoginSerializer
import random
from datetime import datetime, timedelta
from .models import PasswordResetCode
from django.core.mail import send_mail
import secrets




Customer = get_user_model()



class RegisterAPIView(APIView):
    def post(self, request):
        try:
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                tokens = get_tokens_for_user(user)
                response = {
                    "code": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Registration successful",
                    "data": {
                        "user": CustomerSerializer(user).data,
                    
                    }
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error during registration: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "user_id": user.id,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "success": False,
                    "message": "Invalid credentials"
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Login failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    def get(self, request):
        try:
            serializer = CustomerSerializer(request.user)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Profile fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching profile: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            serializer = CustomerSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error updating profile: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerAddressAPIView(APIView):
    def get(self, request):
        try:
            addresses = CustomerAddress.objects.filter(customer=request.user)
            serializer = CustomerAddressSerializer(addresses, many=True)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Addresses fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error fetching addresses: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            data['customer'] = request.user.id
            serializer = CustomerAddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save(customer=request.user)
                response = {
                    "code": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Address added successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error adding address: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        code = str(random.randint(100000, 999999))
        PasswordResetCode.objects.create(email=email, code=code)

        send_mail(
            "Password Reset Code",
            f"Your code is: {code}",
            "no-reply@paakhi.com",
            [email],
            fail_silently=True,
        )

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Reset code sent"
        }, status=status.HTTP_200_OK)


class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            reset = PasswordResetCode.objects.filter(email=email, code=code, is_used=False).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid or expired code"
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
                "message": "Passwords do not match"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset = PasswordResetCode.objects.get(reset_token=token, is_used=True)
        except PasswordResetCode.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid reset token"
            }, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_expired():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Reset token has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Customer.objects.get(email=reset.email)
        except Customer.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Password has been reset successfully."
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(token).blacklist()
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
