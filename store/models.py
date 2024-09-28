from django.core.validators import RegexValidator
from django.db import models


# import barcode
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .Barcode import BarcodeEAN13


class Category(models.Model):
    name = models.CharField(max_length=120)
    comment = models.CharField(max_length=220, blank=True, null=True)

    def __str__(self):
        return self.name


class Sizes(models.Model):
    size = models.CharField(max_length=15)
    def __str__(self):
        return self.size


class GroupedSizes(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + str(self.size)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True)
    color = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=30,unique=True,validators=[
        RegexValidator('^([0-9]{13})|([0]{1})$'
        ),
    ])
    size = models.CharField(max_length=30, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return (self.product.name + " " + str(self.size))




class Stock(models.Model):
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_detail.product.name


class Supplier(models.Model):
    name = models.CharField(max_length=120)
    phone = models.IntegerField()
    comment = models.CharField(max_length=220, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.name)




class SuppliedProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product.name


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    supplied_product = models.ForeignKey(SuppliedProduct, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=220, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.supplier.name



@receiver(pre_save, sender=ProductDetail,)
def setSKU(instance,**kwargs):


            if (instance.sku.strip() =="0"):

                sku = BarcodeEAN13.generateRandom([p.product for p in ProductDetail.objects.all()])
                count = 1
                while(ProductDetail.objects.filter(sku=sku).exists()):
                    sku = BarcodeEAN13.generateRandom()
                    print("found")
                    count =count+1
                    if (count==3):
                        break
                instance.sku = sku
                instance.save()


@receiver(post_save, sender=SuppliedProduct)
def productSupplied(sender, instance, created, **kwargs):
    if created:

           instance.total_cost = instance.unit_cost * instance.quantity
           instance.save()

           prouduct_detail = instance.product
           stock = Stock.objects.filter(product_detail =prouduct_detail)

           # stock doesn't exist product is new
           if(len(stock)==0):
               Stock.objects.create(product_detail=prouduct_detail,quantity=instance.quantity,low_stock_threshold=1)
               prouduct_detail.cost_price = instance.unit_cost
               prouduct_detail.save()
           else:

               stock = stock[0]
               prev_quantity = stock.quantity
               prev_cost_price = prouduct_detail.cost_price

               new_cost_price = ((prev_quantity*prev_cost_price)+(instance.quantity+instance.unit_cost))/(prev_quantity+instance.quantity)
               stock.quantity = stock.quantity + instance.quantity
               prouduct_detail.cost_price = new_cost_price
               prouduct_detail.save()
               stock.save()
