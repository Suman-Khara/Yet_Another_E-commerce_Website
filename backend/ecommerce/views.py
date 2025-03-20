from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import *
from .serializers import *
from rest_framework import views, response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        """
        Optionally filters products by search query (name, category, or tags).
        """
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(category__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        return queryset

class ProductDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            product_data = ProductSerializer(product).data
            reviews = Review.objects.filter(product=product)
            reviews_data = ReviewSerializer(reviews, many=True).data

            # Check if the user has a review for this product
            user_review = reviews.filter(user=request.user.customer).first()
            user_review_data = ReviewSerializer(user_review).data if user_review else None

            return response.Response({
                'product': product_data,
                'reviews': reviews_data,
                'user_review': user_review_data
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return response.Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product__product_id=product_id)

    def perform_create(self, serializer):
        product = Product.objects.get(product_id=self.kwargs['product_id'])
        serializer.save(user=self.request.user.customer, product=product)

class ReviewUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs['product_id']
        username = self.kwargs['username']

        # Ensure only the user can update their own review
        if self.request.user.username != username:
            raise PermissionDenied("You cannot update this review.")
        
        return Review.objects.get(product__product_id=product_id, user__user__username=username)