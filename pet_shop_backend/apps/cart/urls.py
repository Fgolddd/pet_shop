from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.CartView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('products/<int:pk>/checked/', views.CartView.as_view({
        'put':'update_product_status'
    })),
    path('products/<int:pk>/number/', views.CartView.as_view({
        'put':'update_product_number'
    })),
    path('products/<int:pk>/', views.CartView.as_view({
        'delete':'destroy'
    }))
]