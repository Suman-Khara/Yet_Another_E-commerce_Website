from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<str:product_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('products/<str:product_id>/reviews/<str:username>/', ReviewUpdateView.as_view(), name='review-update'),
]
