from rest_framework import serializers

from apps.products.serializers import ProductSerializer
from apps.orders.models import Order, OrderProducts, Comment

class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProducts
        fields = ['product', 'number', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    ordergoods_set = serializers.SerializerMethodField()

    
    class Meta:
        model = Order
        fields = "__all__"
    
    def get_ordergoods_set(self, obj):
        # 在这里自定义返回的ordergoods_set字段数据
        # 可以查询相关的OrderProducts对象，并返回相应的数据
        orderproducts = OrderProducts.objects.filter(order=obj)
        serializer = OrderProductsSerializer(orderproducts, many=True)
        for ordergoods in serializer.data:
            ordergoods['product']['cover'] = 'http://127.0.0.1:8000' + ordergoods['product']['cover']
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'