from django.db import models
from common.db import BaseModel
# Create your models here.

class Order(BaseModel):
    ORDER_STATUS = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
        (6, '已关闭'),

    )
    PAY_TYPES = (
        (1, '支付宝'),
        (2, '微信'),
        (3, '银行卡'),
        (4, '货到付款'),
    )
    user = models.ForeignKey('users.User', verbose_name='用户', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='收货地址', max_length=200)
    order_code = models.CharField(verbose_name='订单编号', max_length=50)
    amount = models.DecimalField(verbose_name='订单金额', max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(verbose_name='订单状态', default=1, choices=ORDER_STATUS)
    pay_type = models.SmallIntegerField(verbose_name='支付方式', default=1, blank=True, choices=PAY_TYPES)
    pay_time = models.DateTimeField(verbose_name='支付时间', blank=True, null=True)
    trade_no = models.CharField(verbose_name='支付单号', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_code

class OrderProducts(BaseModel):
    order = models.ForeignKey('Order', verbose_name='所属订单', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', verbose_name='商品id', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    number = models.IntegerField(verbose_name='商品数量', default=1)

    class Meta:
        db_table = 'order_products'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name

class Comment(BaseModel):
    RATES = (
        (1, '好评'),
        (2, '中评'),
        (3, '差评')
    )
    STARS = (
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星')
    )
    user = models.ForeignKey('users.User', verbose_name='评论用户', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name='所属订单', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', verbose_name='所属商品', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=500, default='')
    rate = models.SmallIntegerField(verbose_name='评论级别', default=1, blank=True, choices=RATES)
    star = models.SmallIntegerField(verbose_name='评论星级', default=1, blank=True, choices=STARS)

    class Meta:
        db_table = 'comment'
        verbose_name = '订单评论'
        verbose_name_plural = verbose_name
