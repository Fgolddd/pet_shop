from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('list/', views.ProductView.as_view({
        'get':'list'
    })),

    path('list/<int:pk>/', views.ProductView.as_view({
        'get':'retrieve'
    })),

    path('collect/', views.CollectView.as_view({
        'get':'list',
        'post':'create'
    })),
    path('collect/<int:pk>/', views.CollectView.as_view({
        'delete':'destroy'
    })),
]