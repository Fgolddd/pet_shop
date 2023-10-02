import re, os

from django.http import FileResponse
from pet_shop.settings import MEDIA_ROOT
from tokenize import TokenError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer
from common.permissions import UserPermission, AddressPermission

# Create your views here.

class UserView(GenericViewSet,mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]

    def upload_avatar(self, request, *args, **kwargs):
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error':'文件不存在！'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if avatar.size > 1024 * 300:
            return Response({'error':'文件过大！'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = self.get_object()
        serializer = self.get_serializer(user, data={'avatar':avatar}, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'url': serializer.data['avatar']})

class FileView(APIView):
    """获取文件的视图"""

    def get(self, requests, name):
        path = MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': "没有找到该文件！"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        password_confirmation = request.data.get('password_confirmation')

        if not all([username, password, phone, password_confirmation]):
            return Response({'error': '参数不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if User.objects.filter(phone=phone).exists():
            return Response({'error': '手机已注册'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if password != password_confirmation:
            return Response({'error': '密码不一致'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not (6 <= len(password) <= 18):
            return Response({'error': '密码长度要在6-18位'}, status=status.HTTP_400_BAD_REQUEST)

        if re.match(r'^1 d {9}$', phone):
            return Response({'error': '手机号码格式错误'}, status=status.HTTP_400_BAD_REQUEST)

        obj = User.objects.create_user(username=username, phone=phone, password=password)
        res = {
            'username': username,
            'id': obj.id,
            'phone': obj.phone
        }

        return Response(res, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['phone'] = serializer.user.phone
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')

        return Response(result, status=status.HTTP_200_OK)
    

class AddressView(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, AddressPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_address(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_default = True
        obj.save()

        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        
        return Response({'message': '设置成功'}, status=status.HTTP_200_OK)
        