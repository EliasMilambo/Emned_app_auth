from django.urls import path
from customers.views import (customer_manager,
                             customer_create,
                             customer_edit,
                             view_info)
urlpatterns = [
    path('customer_manager/', customer_manager, name='customer_manager'),
    path('customer_create/', customer_create, name='customer_create'),
    path('customer_edit/<int:pk>/', customer_edit, name='customer_edit'),
    path('view_info/<int:pk>/', view_info, name='view_info'),
]