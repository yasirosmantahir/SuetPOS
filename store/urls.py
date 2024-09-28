from django.urls import  include, path
from django.views.decorators.csrf import csrf_exempt

from .views import *
#
from rest_framework.routers import DefaultRouter


#router.register(r'grouped-sizes', GroupedSizesViewSet)

urlpatterns = [
    path('products/by-sku/<str:sku>/', GetProductBySkuView.as_view(), name='get_product_by_sku'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('generate-barcode/<str:sku>/',GenerateBarcode.as_view(), name='generate-barcode'),
    path('add-product/',addProduct,name='add-product'),
]
