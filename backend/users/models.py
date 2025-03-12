from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10, unique=True, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    verified=models.BooleanField(default=False)

    def __str__(self):
        return f"Customer: {self.user.username}"
    
class Seller(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10, unique=True, null=True, blank=True)
    store_name=models.CharField(max_length=255)
    store_address=models.TextField(null=True, blank=True)
    verified=models.BooleanField(default=False)

    def __str__(self):
        return f"Seller: {self.user.username} - {self.store_name}"
    
class DeliveryPartner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10, unique=True, null=True, blank=True)
    verified=models.BooleanField(default=False)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"Delivery Partner: {self.user.username}"