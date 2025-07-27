from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.account.models import CustomerAddress
from apps.account.serializers import CustomerSerializer, CustomerRegisterSerializer, CustomerAddressSerializer


Customer = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
                        "tokens": tokens
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
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                tokens = get_tokens_for_user(user)
                response = {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "Login successful",
                    "data": {
                        "user": CustomerSerializer(user).data,
                        "tokens": tokens
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": f"Error during login: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
