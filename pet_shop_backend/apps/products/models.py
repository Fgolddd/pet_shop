from django.db import models
from common.db import BaseModel
from ckeditor.fields import RichTextField
# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name='分类', max_length=20)
    image = models.ImageField(verbose_name='分类图标',upload_to='category/', blank=True, null=True)
    status = models.BooleanField(verbose_name='是否启用', default=False)

    class Meta:
        db_table = 'category'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name
    
    
    def __str__(self):
        return self.name
    
    

class Product(models.Model):
    RECOMEND_INDEX = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
        (5, '五级')
    )
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=20, default='')
    desc = models.CharField(verbose_name='商品描述', max_length=29, default='')
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)
    cover = models.ImageField(verbose_name='图片连接', upload_to='product/', blank=True, null= True)
    stock = models.IntegerField(verbose_name='库存', default=0, blank=True)
    sales = models.IntegerField(verbose_name='销量', default=0, blank=True)
    is_on = models.BooleanField(verbose_name='是否上架', default=False, blank=True)
    recommend = models.SmallIntegerField(verbose_name='推荐指数', default=1, blank=True, choices=RECOMEND_INDEX)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name
    
    

class Detail(BaseModel):
    product = models.OneToOneField('Product', verbose_name='商品', on_delete=models.CASCADE)
    vender = models.ForeignKey('users.User', verbose_name='商家', on_delete=models.CASCADE)
    details = RichTextField(verbose_name='详情', blank=True)

    class Meta:
        db_table = 'detail'
        verbose_name = '商品详情'
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    title = models.CharField(verbose_name='轮播图名称', max_length=20, blank=True, default='')
    image = models.ImageField(verbose_name='轮播图连接', upload_to='banner/', blank=True, null=True)
    status = models.BooleanField(verbose_name='是否启用', default=False)
    seq = models.IntegerField(verbose_name='顺序', default=1, blank=True)

    class Meta:
        db_table = 'banner'
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title

class Collect(models.Model):
    user = models.ForeignKey('users.User', verbose_name='用户', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name='商品', on_delete=models.CASCADE)

    class Meta:
        db_table = 'collect'
        verbose_name = '收藏商品'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.product