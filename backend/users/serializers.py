from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'phone_number', 'address']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class CustomerSignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField()
    address = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        customer = Customer.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            address=validated_data['address']
        )
        return customer

class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user=serializers.HiddenField(default=None)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        data["user"] = user
        return data
    
class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'address']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['store_name', 'store_email', 'store_address', 'phone_number', 'verified']

class SellerSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Seller
        fields = ['store_name', 'store_email', 'store_address', 'phone_number', 'password']

    def validate_store_email(self, value):
        """Ensure unique email"""
        if Seller.objects.filter(store_email=value).exists():
            raise serializers.ValidationError("A seller with this email already exists.")
        return value

    def create(self, validated_data):
        """Create a new seller with a hashed password"""
        password = validated_data.pop('password')
        seller = Seller(**validated_data)
        seller.set_password(password)  # Hash password before saving
        seller.save()
        return seller

class SellerLoginSerializer(serializers.Serializer):
    store_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate seller"""
        email = data.get("store_email")
        password = data.get("password")

        try:
            seller = Seller.objects.get(store_email=email)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not seller.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        # Generate or retrieve a custom token for the seller
        token, _ = SellerToken.objects.get_or_create(seller=seller)

        data["seller"] = seller
        data["token"] = token.token
        return data

class SellerProfileSerializer(serializers.ModelSerializer):
    store_name = serializers.ReadOnlyField()
    store_email = serializers.ReadOnlyField()

    class Meta:
        model = Seller
        fields = ['store_name', 'store_email', 'store_address', 'phone_number', 'verified']
