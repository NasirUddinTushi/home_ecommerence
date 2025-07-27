from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import CustomerAddress

Customer = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'avatar_url', 'is_guest', 'is_active', 'date_joined'
        ]

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            'id', 'full_name', 'phone', 'address_line1', 'address_line2',
            'city', 'state', 'zip_code', 'country', 'is_default'
        ]
