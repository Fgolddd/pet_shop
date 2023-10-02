from django.contrib.auth.backends import BaseBackend
from apps.users.models import User
from django.db.models import Q
from rest_framework import serializers
class MyBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phone=username))
            
        except:
            raise serializers.ValidationError({'error': '未找到该用户！'})
        else:
            if user.check_password(password):
                return user
            else: 
                raise serializers.ValidationError({'error': '密码错误！'})
