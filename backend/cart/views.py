from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from ecommerce.models import Product
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        product_id = request.data.get('product_id')
        product = Product.objects.get(product_id=product_id)
        customer = request.user.customer
        
        # Ensure the customer has a cart
        cart, created = Cart.objects.get_or_create(user=customer)

        # Check if the product already exists in the cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        # Check stock availability
        if not item_created and cart_item.quantity + 1 > product.stock:
            return Response({'error': 'Cannot add more items than available stock.'}, status=400)

        if item_created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        
        cart_item.save()
        return Response({'message': 'Product added to cart successfully'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    customer = request.user.customer
    cart, _ = Cart.objects.get_or_create(user=customer)

    cart_items = cart.items.select_related('product').all()
    data = [
        {
            "id": item.id,
            "product_id": item.product.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "stock": item.product.stock,
            "total_price": item.total_price()
        }
        for item in cart_items
    ]

    return Response({"cart_items": data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    customer = request.user.customer
    product = get_object_or_404(Product, product_id=request.data.get('product_id'))
    quantity = int(request.data.get('quantity'))

    if quantity <= 0:
        return Response({"error": "Quantity must be at least 1."}, status=400)

    if quantity > product.stock:
        return Response({"error": "Requested quantity exceeds available stock."}, status=400)

    cart = get_object_or_404(Cart, user=customer)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()

    return Response({"message": "Cart item updated successfully."})


# Remove Cart Item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    customer = request.user.customer
    product = get_object_or_404(Product, product_id=request.data.get('product_id'))
    cart = get_object_or_404(Cart, user=customer)

    CartItem.objects.filter(cart=cart, product=product).delete()

    return Response({"message": "Item removed from cart."})