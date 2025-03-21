from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

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

class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, product_id=product_id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)

class AddToCartView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, product_id=product_id)
        
        if product.stock < 1:
            return Response({'error': 'Product is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the customer's cart
        customer = user.customer
        cart, created = Cart.objects.get_or_create(user=customer)

        # Get or create a CartItem for the product in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not item_created:
            # If the cart item already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def test_post(request):
    # Simply echo back the received data
    data = request.data
    print("Received data:", data)
    return Response({'message': 'Test successful!', 'data_received': data}, status=status.HTTP_200_OK)

@csrf_exempt  # For testing purposes; remove in production if CSRF is properly handled
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_review(request):
    serializer = SubmitReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Review submitted successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
