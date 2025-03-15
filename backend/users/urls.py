from django.urls import path
from .views import *

urlpatterns = [
    # Customer Endpoints
    path('signup/customer', customer_signup, name='customer-signup'),
    path("login/customer", customer_login, name="customer_login"),
    path("customer/profile/<str:username>/", customer_profile, name="customer_profile"),
    path("customer/profile/update/<str:username>/", update_customer_profile, name="update_customer_profile"),

    # Seller Endpoints
    path('signup/seller', seller_signup, name='seller-signup'),
    path("login/seller", seller_login, name="seller_login"),
    path("seller/profile/<str:store_name>/", seller_profile, name="seller_profile"),
    path("seller/profile/update/<str:store_name>/", update_seller_profile, name="update_seller_profile"),
]