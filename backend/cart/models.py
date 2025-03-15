from django.db import models
from users.models import Customer
from ecommerce.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)  # Each user has 1 cart
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        """Calculate total price with discount applied"""
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Calculate total price for this item"""
        return self.product.discounted_price() * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"