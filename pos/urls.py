from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *
from . import views

urlpatterns = [

    path('orders/create/', CreateOrderView, name='create_order'),
    path('orders/void/', VoidOrderItemsView.as_view(), name='void_order'),
    path('sales/', views.sales, name='sales'),
    path('help/', views.help, name="help"),
]