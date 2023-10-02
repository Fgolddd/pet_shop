from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import CartSerializer, CartReadSerializer
from apps.cart.models import Cart
from common.permissions import CartPermission

class CartView(GenericViewSet, mixins.DestroyModelMixin, 
               mixins.CreateModelMixin, mixins.ListModelMixin,
               mixins.UpdateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, CartPermission]

    filter_fields = ['is_checked']

    def get_serializer_class(self):
        if self.action == 'list':
            return CartReadSerializer
        else:
            return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        user = request.user
        product = request.data.get('product')

        if Cart.objects.filter(user=user, product=product).exists():
            cart_product = Cart.objects.get(user=user, product=product)
            cart_product.number += 1
            cart_product.save()
            
            serializer = self.get_serializer(cart_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            request.data['user'] = user.id
            return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)

        serialzier = self.get_serializer(queryset, many=True)
        return Response(serialzier.data)

    def update_product_status(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_checked = not obj.is_checked
        obj.save()
        return Response({'message', '修改成功'}, status=status.HTTP_200_OK)
    
    def update_product_number(self, request, *args, **kwargs):
        number = request.data.get('number')
        obj = self.get_object()

        if not isinstance(number, int):
            return Response({'error': '参数只能是数字，且不能为空'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if number <= 0:
            obj.delete()
            return Response({'message': "修改成功,数量小于1，已经从购物车移除该商品"},
                            status=status.HTTP_200_OK)    
        else:
            obj.number = number
            obj.save()
            return Response({'message': "修改成功"},
                            status=status.HTTP_200_OK)
    

