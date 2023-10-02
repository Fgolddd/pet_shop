from apps.products.serializers import CartProductSerializer
from .models import Cart
from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"

class CartReadSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = Cart
        fields = "__all__"


