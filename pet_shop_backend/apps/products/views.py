from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from .models import Product, Category, Banner, Collect, Detail
from .serializers import CollectReadSerializer, ProductSerializer, CategorySerializer, BannerSerializer, CollectSerializer, DetailSerializer
from common.permissions import CollectPermission
# Create your views here.

class IndexView(APIView):
    def get(self, request):
        category = Category.objects.filter(status=True)
        category_serializer = CategorySerializer(category, many=True, context={'request': request})

        banner = Banner.objects.filter(status=True)
        banner_serializer = BannerSerializer(banner, many=True, context={'request': request})

        product = Product.objects.filter(is_on=True, recommend=True).order_by('category')
        product_serializer = ProductSerializer(product, many=True, context={'request': request})

        result = dict(
            category=category_serializer.data,
            banner=banner_serializer.data,
            product=product_serializer.data
        )

        return Response(result)


class ProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_on=True)
    serializer_class = ProductSerializer

    filterset_fields = ('category', 'recommend')
    ordering_fields = ('sales', 'price', 'id')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data

        try:
            detail = Detail.objects.get(product=instance)
            detail_serializer = DetailSerializer(detail)
            result['detail'] = detail_serializer.data
        except Exception as e:
            result['detail'] = {
                'vender':'',
                'details':''
            }
        
        return Response(result)
    
class CollectView(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated, CollectPermission]

    def create(self, request, *args, **kwargs):
        user = request.user
        user_id = request.data.get('user')

        if user.id != user_id:
            return Response({'error':'没有操作该用户的权限'}, status=status.HTTP_403_FORBIDDEN)
        
        product = request.data.get('product')
        if not product:
            return Response({'error':'参数product不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if self.queryset.filter(user=user, product=product).exists():
            return Response({'error':'商品已收藏'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return super().create(request, *args, **kwargs)    
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)

        serializer = CollectReadSerializer(queryset, many=True, context={'request':request})

        return Response(serializer.data)


