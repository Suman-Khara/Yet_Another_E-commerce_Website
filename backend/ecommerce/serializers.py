from rest_framework import serializers
from .models import *

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'stock', 'category', 'tags', 'discount', 'rating', 'image_url', 'thumbnail_url']

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.store_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['username', 'rating', 'comment', 'created_at']