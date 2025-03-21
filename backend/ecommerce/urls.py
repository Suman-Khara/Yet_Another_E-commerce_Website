from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('products/review/', submit_review, name='submit-review'), 
    path('test/', test_post, name='test-post'),
]