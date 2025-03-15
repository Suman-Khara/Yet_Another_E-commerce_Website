from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import secrets

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10, unique=True, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    verified=models.BooleanField(default=False)

    def __str__(self):
        return f"Customer: {self.user.username}"
    
class Seller(models.Model):
    store_name = models.CharField(max_length=255)
    store_email = models.EmailField(unique=True)
    store_address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    
    def set_password(self, raw_password):
        """Hash and store password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Seller: {self.store_name}"
    
class SellerToken(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True, default=secrets.token_hex)

    def regenerate_token(self):
        """Generate a new token"""
        self.token = secrets.token_hex()
        self.save()

    def __str__(self):
        return f"Token for {self.seller.store_email}"
    
class DeliveryPartner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10, unique=True, null=True, blank=True)
    verified=models.BooleanField(default=False)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"Delivery Partner: {self.user.username}"