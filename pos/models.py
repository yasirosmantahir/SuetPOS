from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from store.models import ProductDetail,Stock

from django.conf import settings


class Order(models.Model):

    total_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    isvoid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    isvoid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at) + str(self.stock.product_detail)


