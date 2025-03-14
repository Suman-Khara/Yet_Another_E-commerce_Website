from django.db import models
from users.models import *
import uuid

def generate_order_id():
    return str(uuid.uuid4())[:12].replace("-", "").upper()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Auto or Manual ID
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Link to Seller
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)  # Many-to-Many for flexible tagging
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rating = models.FloatField(default=0.0)  # Average rating based on reviews
    total_reviews = models.PositiveIntegerField(default=0)  # Number of reviews
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.seller.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer who left the review
    rating = models.PositiveIntegerField()  # Rating (1-5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for the review

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} - {self.rating}★"
    
class Order(models.Model):
    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    order_id = models.CharField(max_length=20, unique=True, editable=False)  # Auto-generate
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.user.username} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()  # Function to generate order IDs
        super().save(*args, **kwargs)

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS)

    def __str__(self):
        return f"History for Order {self.order.order_id} - {self.status}"
