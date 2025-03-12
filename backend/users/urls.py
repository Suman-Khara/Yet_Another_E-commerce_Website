from django.urls import path
from .views import *

urlpatterns = [
    path('signup/customer', customer_signup, name='customer-signup'),
    path("login/customer", customer_login, name="customer_login"),
    path("customer/profile/<str:username>/", customer_profile, name="customer_profile"),
    path("customer/profile/update/<str:username>/", update_customer_profile, name="update_customer_profile"),
]