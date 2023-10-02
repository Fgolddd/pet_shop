from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
# yasg的视图配置类，用于生成a'pi
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="drf接口文档",  # 必传
        default_version='v1.0,0',  # 必传
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include('apps.users.urls')),
    path("api/products/", include('apps.products.urls')),
    path("api/cart/", include('apps.cart.urls')),
    path("api/orders/", include('apps.orders.urls')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # 添加UI视图
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # 添加UI视图
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
