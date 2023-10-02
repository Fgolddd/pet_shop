from django.db import models
from django.contrib.auth.models import AbstractUser
from common.db import BaseModel
# Create your models here.

class User(AbstractUser, BaseModel):
    phone = models.CharField(verbose_name='手机号', default='', max_length=11)
    avatar = models.ImageField(verbose_name='用户头像',upload_to='avatar/', blank=True, null=True)
    is_seller = models.BooleanField(verbose_name='是否为商家', default=False)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

class Address(models.Model):
    user = models.ForeignKey('User', verbose_name='所属用户', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    name = models.CharField(verbose_name='收货人', max_length=20)
    province = models.CharField(verbose_name='省份', max_length=20)
    city = models.CharField(verbose_name='城市', max_length=20)
    county = models.CharField(verbose_name='区县', max_length=20)
    address = models.CharField(verbose_name='详细地址', max_length=100)
    is_default = models.BooleanField(verbose_name='是否为默认地址', default=False)

    class Meta:
        db_table = 'address'
        verbose_name = '收货地址表'
        verbose_name_plural = verbose_name

class Area(models.Model):
    pid = models.IntegerField(verbose_name='上级id')
    name = models.CharField(verbose_name='地区名', max_length=20)
    level = models.IntegerField(verbose_name='区域等级')

    class Meta:
        db_table = 'area'
        verbose_name = '地区表'
        verbose_name_plural = verbose_name

class VeriCode(models.Model):
    phone = models.CharField(verbose_name='手机号', max_length=11)
    code = models.CharField(verbose_name='验证码', max_length=11)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'vericode'
        verbose_name = '验证码表'
        verbose_name_plural = verbose_name