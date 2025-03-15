from django.urls import path
from .views import *

urlpatterns = [
    # Customer Endpoints
    path('customer/signup/', customer_signup, name='customer-signup'),
    path("customer/login/", customer_login, name="customer_login"),
    path("customer/profile/<str:username>/", customer_profile, name="customer_profile"),
    path("customer/profile/update/<str:username>/", update_customer_profile, name="update_customer_profile"),

    # Seller Endpoints
    path('seller/signup/', seller_signup, name='seller-signup'),
    path("seller/login/", seller_login, name="seller_login"),
    path("seller/profile/<str:store_name>/", seller_profile, name="seller_profile"),
    path("seller/profile/update/<str:store_name>/", update_seller_profile, name="update_seller_profile"),

    # Delivery Partner Endpoints
    path('delivery/signup/', delivery_signup, name='delivery-signup'),
    path("delivery/login/", delivery_login, name="delivery_login"),
    path("delivery/profile/<str:username>/", delivery_profile, name="delivery_profile"),
    path("delivery/profile/update/<str:username>/", update_delivery_profile, name="update_delivery_profile"),
]