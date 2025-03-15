from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@api_view(['POST'])
def customer_signup(request):
    print("Received data:", request.data)  # Log incoming data
    serializer = CustomerSignUpSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)
    
    print("Signup errors:", serializer.errors)  # Log errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def customer_login(request):
    serializer = CustomerLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,  # Include username in response
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def customer_profile(request, username):
    try:
        user = User.objects.get(username=username)
        customer = Customer.objects.get(user=user)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data)
    except (User.DoesNotExist, Customer.DoesNotExist):
        return Response({"error": "User not found"}, status=404)

#@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_customer_profile(request, username):
    try:
        user = User.objects.get(username=username)  # Find user by username
        customer = Customer.objects.get(user=user)  # Get corresponding customer profile
        
        serializer = CustomerProfileSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def seller_signup(request):
    serializer = SellerSignUpSerializer(data=request.data)

    if serializer.is_valid():
        seller = serializer.save()
        # Generate token for the new seller
        token = SellerToken.objects.create(seller=seller)
        return Response({"message": "Signup successful!", "token": token.token}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def seller_login(request):
    serializer = SellerLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            {
                "token": serializer.validated_data["token"],
                "store_name": serializer.validated_data["seller"].store_name,
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def seller_profile(request, store_name):
    """Fetch seller profile by store name"""
    try:
        seller = Seller.objects.get(store_name=store_name)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SellerProfileSerializer(seller)
    print("Profile Data:", serializer.data)  # Debugging log
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_seller_profile(request, store_name):
    """Update seller profile using store_name from URL"""
    try:
        seller = Seller.objects.get(store_name=store_name)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SellerProfileSerializer(seller, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)