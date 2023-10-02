from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderView.as_view({
        'get':'list'
    })),
    path('submit/', views.OrderView.as_view({
        'post':'create'
    })),
    path('order/<int:pk>/', views.OrderView.as_view({
        'get':'retrieve',
        'put':'close_order'

    })),
    path('order/pay/<int:pk>/', views.OrderView.as_view({
        'put':'pay_order',
    })),
    path('order/confirm/<int:pk>/', views.OrderView.as_view({
        'put':'confirm_order',
    })),
    path('comment/', views.CommentView.as_view({
        'post':'create',
        'get':'list',
                
    })),
    path('payment/alipay/', views.OrderPayView.as_view({
        'post':'create',
        'get':'get_pay_result'
    })),
    # path('payment/alipay/callback/', views.OrderPayView.as_view({
    #     'post': "alipay_callback_result",
    # })),
]