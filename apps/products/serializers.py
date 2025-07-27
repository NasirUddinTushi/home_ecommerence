from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, Attribute, AttributeValue, ProductVariantValue


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class ProductVariantValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute_value.attribute.name', read_only=True)
    attribute_value = serializers.CharField(source='attribute_value.value', read_only=True)

    class Meta:
        model = ProductVariantValue
        fields = ['id', 'attribute_name', 'attribute_value']


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_values = ProductVariantValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'stock', 'price_override', 'variant_values']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category_name', 'price', 'is_featured', 'images', 'variants']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
