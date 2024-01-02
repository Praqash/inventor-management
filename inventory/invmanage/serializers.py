from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductAllocation

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAllocation
        fields = ["quantity_allocated", "allocated_to"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerializer(many=True, read_only=True)
    allocations = AllocationSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ["id", "category", "name", "description", "slug", "product_image", "total_count", "remaining_count", "allocations"]

