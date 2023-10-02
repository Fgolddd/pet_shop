from django.db import models
from common.db import BaseModel
# Create your models here.

class Cart(BaseModel):
    user = models.ForeignKey('users.User', verbose_name='用户', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', verbose_name='商品', on_delete=models.CASCADE)
    number = models.SmallIntegerField(verbose_name='数量', default=1, blank=True)
    is_checked = models.BooleanField(verbose_name='是否选中', default=True, blank=True)

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name