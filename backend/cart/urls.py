from django.urls import path
from .views import *

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('update/', update_cart_item, name='update_cart_item'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
