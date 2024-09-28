from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'comment',
    list_filter = ('name', 'comment',)
    search_fields = ('name', 'comment',)


class ProductAdmin(ImportExportModelAdmin):
    list_display = 'name', 'color', 'description', 'category', 'image','is_active', 'created_at', 'updated_at',
    list_filter = ('name', 'color',  'category', 'is_active', 'created_at', 'updated_at',)
    search_fields = ('name', 'color',  'is_active',)


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'size', 'cost_price', 'unit_price', 'created_at', 'updated_at','generate',)
    list_filter = ('product__name', 'sku', 'size','created_at', 'updated_at',)
    search_fields = ('product__id',)
    fields = [
        'product', 'size','sku',
        'cost_price', 'unit_price',
    ]

    def generate(self, obj):
        print(obj.sku)

        link = reverse('generate-barcode', args=[obj.sku])
        print(link)
        html = '<input type="button"  style="padding: 0.2rem; width:100%; vertical-align: top;" onclick="location.href=\'{}\'" value="SKU" />'.format(link)
        return format_html(html)



class StockAdmin(admin.ModelAdmin):
    list_display = 'product_detail', 'quantity', 'low_stock_threshold', 'created_at', 'updated_at',
    list_filter = ('product_detail__product__category__name', 'quantity', 'low_stock_threshold','created_at', 'updated_at',)
    search_fields = ('product_detail__sku','product_detail__size', 'quantity', 'low_stock_threshold','created_at', 'updated_at',)

class SuppliedProductAdmin(admin.ModelAdmin):
    list_display = 'supplier', 'product',  'quantity', 'unit_cost', 'total_cost', 'created_at', 'updated_at',
    list_filter = ('supplier__name', 'product__product__name','created_at', 'updated_at',)
    search_fields = ('supplier__name','product__size','product__product__name','created_at', 'updated_at',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = 'name', 'phone',  'comment', 'created_at', 'updated_at',
    list_filter = ('name', 'phone',)
    search_fields = ('name', 'phone',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'supplier',  'supplied_product', 'amount', 'reference_number','created_at',)
    list_filter = ('supplier','supplier__phone', 'supplied_product','created_at')
    search_fields = ('supplier__name', 'supplier__phone', 'supplied_product', 'reference_number',)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(SuppliedProduct, SuppliedProductAdmin)

admin.site.register(Sizes)
admin.site.register(GroupedSizes)
