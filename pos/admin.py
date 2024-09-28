from django.contrib import admin

# Register your models here.

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = 'user', 'total_amount', 'created_at', 'updated_at', 'isvoid',
    list_filter = ('user', 'isvoid', 'total_amount', 'created_at', 'updated_at',)
    search_fields = ('user', 'total_amount', 'created_at', 'updated_at',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = 'order', 'stock', 'quantity', 'unit_price', 'cost_price', 'created_at', 'updated_at', 'isvoid',
    list_filter = ('isvoid', 'order', 'stock', 'created_at', 'updated_at',)
    search_fields = ('order', 'stock', 'created_at', 'updated_at',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
