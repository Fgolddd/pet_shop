# Generated by Django 4.2.2 on 2023-09-16 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0002_alter_collect_product"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="更新时间"),
                ),
                ("is_delete", models.BooleanField(default=False, verbose_name="删除标记")),
                (
                    "number",
                    models.SmallIntegerField(blank=True, default=0, verbose_name="数量"),
                ),
                (
                    "is_checked",
                    models.BooleanField(blank=True, default=True, verbose_name="是否选中"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="商品",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "购物车",
                "verbose_name_plural": "购物车",
                "db_table": "cart",
            },
        ),
    ]