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

class ProductCategoryInlineSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = ProductCategoryInlineSerializer(read_only=True) 

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'category',    
            'price',
            'is_featured',
            'images',
            'variants'
        ]



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'subcategories']

# Multilevel sub-category

class RecursiveCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'subcategories']

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return RecursiveCategorySerializer(obj.subcategories.all(), many=True).data
        return []
