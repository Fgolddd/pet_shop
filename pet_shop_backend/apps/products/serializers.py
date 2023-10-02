from rest_framework import serializers
from .models import Product, Category, Banner, Detail, Collect

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'cover']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'status', 'is_delete']

class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Detail
        fields = ['vender', 'details']

class CollectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = '__all__'

class CollectReadSerializer(serializers.ModelSerializer):
    """商品收藏序列化器"""
    goods = ProductSerializer()

    class Meta:
        model = Collect
        fields = "__all__"