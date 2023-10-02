import datetime
import time

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from apps.cart.models import Cart
from apps.users.models import Address
from common.permissions import OrderPermission, CommentPermission
from common.payment import Pay

from .models import Order, OrderProducts, Comment
from .serializers import OrderSerializer, OrderProductsSerializer, CommentSerializer

class OrderView(GenericViewSet, mixins.ListModelMixin):
    queryset = Order.objects.all().order_by('-created_time')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]
    filterset_fields = ['status']
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        address = request.data.get('address')
        if not Address.objects.filter(id=address, user=request.user).exists():
            return Response({'error': "订单创建失败，传入的收货地址ID有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        address_obj = Address.objects.get(id=address)
        address_str = '{}{}{}{}  {}   {}'.format(address_obj.province, address_obj.city,
                                              address_obj.county, address_obj.address,
                                              address_obj.name, address_obj.phone)

        cart_products = Cart.objects.filter(user=request.user, is_checked=True)
        if not cart_products.exists():
            return Response({'error': "订单创建失败，未选中商品"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        order_code = str(int(time.time())) + str(request.user.id)
                
        save_id = transaction.savepoint()
        
        try:
            # 创建订单
            order = Order.objects.create(user=request.user, address=address_str,
                                            order_code=order_code, amount=0)

            # 保存商品总价
            amount = 0
            # 遍历购物车中选中所有的商品
            for cart in cart_products:
                # 获取购买商品的数量
                num = cart.number
                # 获取商品的价格
                price = cart.product.price
                # 将价格进行累加
                amount += price * num
                # 判断商品购买数量是否大于商品库存
                if cart.product.stock >= num:
                    # 修改商品的库存和销量并且保存
                    cart.product.stock -= num
                    cart.product.sales += num
                    cart.product.save()
                else:
                    # 事务回滚
                    transaction.savepoint_rollback(save_id)
                    return Response({'error': "创建失败，商品`{}`库存不足".format(cart.product.name)},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                # 在订单商品表中新增一条数据
                OrderProducts.objects.create(order=order, product=cart.product,
                                            price=price, number=num)

                # 删除购物车中该商品记录
                cart.delete()
            # 修改订单的金额
            order.amount = amount
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return Response({'error': "服务处理异常，订单创建失败！"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            transaction.savepoint_commit(save_id)
            # 返回结果
            serializer = self.get_serializer(order)
            # res = {
            #     'order_code': serializer.data['order_code'],
            #     'address': serializer.data['address'],
            #     'amount': serializer.data['amount'],
            #     'status': serializer.data['status'],
            #     'user': serializer.data['user']
            # }
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = self.get_serializer(instance)
        products = OrderProducts.objects.filter(order=instance)
        order_products = OrderProductsSerializer(products, many=True)
        
        result = serializer.data
        result['products_list'] = order_products.data

        return Response(result)

    def close_order(self, request, *args, **kwargs):
        """关闭订单"""
        # 获取到订单对象
        obj = self.get_object()
        # 校验订单是否处于未支付的状态
        if obj.status != 1:
            return Response({'error': "只能取消未支付的订单"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 将订单状态改为关闭
        obj.status = 6
        # 保存
        obj.save()
        # 返回结果
        return Response({'message': "取消成功，已关闭订单"})
    
    def pay_order(self, request, *args, **kwargs):
        """关闭订单"""
        # 获取到订单对象
        obj = self.get_object()
        # 校验订单是否处于未支付的状态
        if obj.status != 1:
            return Response({'error': "只能支付未支付的订单"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 将订单状态改为关闭
        obj.status = 2
        # 保存
        obj.save()
        # 返回结果
        return Response({'message': "支付成功"})
    
    def confirm_order(self, request, *args, **kwargs):
        """关闭订单"""
        # 获取到订单对象
        obj = self.get_object()
        # 校验订单是否处于未支付的状态
        if obj.status != 3:
            return Response({'error': "只能确认待收货的订单"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 将订单状态改为关闭
        obj.status = 4
        # 保存
        obj.save()
        # 返回结果
        return Response({'message': "确认收货成功"})
    
class CommentView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]
    # 配置查询评价信息的过滤参数
    filterset_fields = ['product', 'order']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """商品评价的接口"""
        # 获取参数
        order = request.data.get('order')
        # 校验订单编号是否为空
        if not order:
            return Response({'error': "订单id不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 订单是否存在，并且订单处于`待评价`的状态
        if not Order.objects.filter(id=order).exists():
            return Response({'error': "订单ID有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order_obj = Order.objects.get(id=order)
        if order_obj.user != request.user:
            return Response({'error': "没有评论该订单的权限！"}, status=status.HTTP_403_FORBIDDEN)
        if order_obj.status != 4:
            return Response({'error': "订单不处于待评论状态！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 获取订单评论详情参数
        comment = request.data.get('comment')
        if not isinstance(comment, list):
            return Response({'error': "评论参数comment格式有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 设置一个事务保存的节点
        save_id = transaction.savepoint()

        try:
            for item in comment:
            # 遍历参数中的商品评论信息
            # 校验参数是否有误！
                if not isinstance(item, dict):
                    return Response({'error': "订单评论参数comment格式有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                # 获取当前这条评论信息的商品id
                product = item.get('product', None)
                if not OrderProducts.objects.filter(order=order_obj, product=product).exists():
                    return Response({'error': "订单中没有id为{}的商品！".format(product)},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                # 往item中添加订单id和用户id
                item['user'] = request.user.id
                item['product'] = product
                print(item)
                # 添加一条评论记录
                ser = CommentSerializer(data=item)
                ser.is_valid()
                ser.save()


        # 修改订单的状态为已完成
        # order_obj.status = 5
        # order_obj.save()    
            
        except Exception as e:
            # 事务回滚
            transaction.savepoint_rollback(save_id)
            return Response({'error': "评论失败"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        else:
            # 提交事务
            transaction.savepoint_commit(save_id)
            return Response({'message': "评论成功"}, status=status.HTTP_201_CREATED)


class OrderPayView(GenericViewSet):
    """订单支付接口"""
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """获取支付宝支付页面地址"""
        order_id = request.data.get('orderID')
        if not Order.objects.filter(id=order_id, user=request.user).exists():
            return Response('订单编号有误！', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 查询当前订单
        order = Order.objects.get(id=order_id)
        # 获取订单的总金额
        amount = str(order.amount)
        # 获取订单的编号
        order_on = order.order_code
        # 生成支付宝支付的页面地址
        pay_url = Pay().mobile_pay_url(order_on, amount)

        return Response({'pay_url': pay_url, 'message': "OK"}, status=status.HTTP_200_OK)

    def get_pay_result(self, request):
        """获取支付结果"""
        # 获取参数
        order_code = request.query_params.get('order_code')
        if not Order.objects.filter(order_code=order_code).exists():
            return Response({"message": "订单编号有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order = Order.objects.get(order_code=order_code)
        if order.status != 1:
            return Response({"message": "该订单不处于支付"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 调用支付宝的接口查询订单支付结果
        result = Pay().get_pay_result(order.order_code)
        if result['trade_status'] == 'TRADE_SUCCESS':
            # 修改支付的状态
            order.status = 2
            order.pay_type = 1
            order.pay_time = datetime.datetime.now()
            order.trade_no = result['trade_no']
            # 保存
            order.save()
        return Response(result, status=status.HTTP_200_OK)

    def alipay_callback_result(self, request):
        """支付宝支付成功之后的回调接口(给支付宝调用的)"""

        # 获取支付宝传递过来的回调参数

        # 解析数据并校验身份

        # 修改订单的支付状态

        return Response(status=status.HTTP_200_OK)