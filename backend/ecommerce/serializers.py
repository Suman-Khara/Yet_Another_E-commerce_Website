from rest_framework import serializers
from .models import *
from cart.models import *

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'stock', 'category', 'tags', 'discount', 'rating', 'image_url', 'thumbnail_url']

class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='seller.store_name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'name', 'description', 'price', 'stock', 'category',
            'tags', 'discount', 'rating', 'total_reviews', 'image_url', 'thumbnail_url', 'store_name'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']

class ProductDetailSerializer(ProductSerializer):
    user_review = serializers.SerializerMethodField()
    other_reviews = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['user_review', 'other_reviews']

    def get_user_review(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        review = Review.objects.filter(product=obj, user=user).first()
        return ReviewSerializer(review).data if review else None

    def get_other_reviews(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            reviews = Review.objects.filter(product=obj).exclude(user=user).order_by('-created_at')
        else:
            reviews = Review.objects.filter(product=obj).order_by('-created_at')
        return ReviewSerializer(reviews, many=True).data
    
class SubmitReviewSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_product_id(self, value):
        try:
            # Ensure the product exists
            product = Product.objects.get(product_id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(product_id=validated_data['product_id'])
        # Use the customer linked to the request's user
        customer = self.context['request'].user.customer
        review, created = Review.objects.update_or_create(
            product=product,
            user=customer,
            defaults={
                'rating': validated_data['rating'],
                'comment': validated_data.get('comment', '')
            }
        )
        # Update product's average rating and review count
        all_reviews = product.reviews.all()
        total_reviews = all_reviews.count()
        avg_rating = sum(r.rating for r in all_reviews) / total_reviews if total_reviews else 0
        product.rating = avg_rating
        product.total_reviews = total_reviews
        product.save()
        return review