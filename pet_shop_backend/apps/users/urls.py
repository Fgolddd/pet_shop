from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import LoginView, RegisterView, UserView, FileView, AddressView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('<int:pk>/', UserView.as_view({'get':'retrieve'})),
    path('<int:pk>/avatar/upload/', UserView.as_view({'post':'upload_avatar'})),

    path('address/', AddressView.as_view({
        'get': 'list',
        'post': 'create',
    })),

    path('address/<int:pk>/', AddressView.as_view({
        'put': 'update',    
        'delete': 'destroy',
    })),

    path('address/<int:pk>/default/', AddressView.as_view({'put': 'set_default_address'})),


    re_path(r'media/(.+?)/', FileView.as_view()),

]
