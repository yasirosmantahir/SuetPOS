from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import *

from django.http import JsonResponse
from pandas.core.indexes import category
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, ProductDetail, Stock ,SuppliedProduct
from .forms import ProductForm, CategoryForm

from django.contrib import admin
from .models import GroupedSizes


class GetProductBySkuView(View):
    """
    Fetch the product and its associated details by the given SKU.
    """
    def get(self, request, sku):
        print(sku)
        try:
            # Fetch the product detail record by the given SKU

            product_detail = ProductDetail.objects.get(sku=sku)

            # Fetch the product record
            product = product_detail.product

            # Fetch the stock information for the product detail
            #stock = Stock.objects.get(product_detail=product_detail)

            img = product.image.url if product.image != "" else ""
            # Prepare the response
            product_data = {
                "id": product_detail.id,
                "name": product.name,
                "color": product.color,
                "description": product.description,
                "category_id": product.category_id,
                "sku": product_detail.sku,
                "unit_price": product_detail.unit_price,
                #"cost_price": stock.cost_price,
                "image":  img,
                "is_active": product.is_active,
                "size": product_detail.size,
                #"quantity": stock.quantity,
                #"low_stock_threshold": stock.low_stock_threshold
            }

            return JsonResponse(product_data)

        except ProductDetail.DoesNotExist:
            # Handle the case where the product detail is not found
            return JsonResponse({"error": "Product Detail not found."}, status=404)
        except (Product.DoesNotExist):
            # Handle the case where the product or stock information is not found
            return JsonResponse({"error": "Product not found."}, status=404)

        except (Stock.DoesNotExist):
            # Handle the case where the product or stock information is not found
            return JsonResponse({"error": "stock information not found."}, status=404)
        except(Exception):
            return JsonResponse({"error": "Internal server error"}, status=404)


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = ProductDetail

class GenerateBarcode(View):
    def get(self,request,sku):
        product_detail =get_object_or_404(ProductDetail,sku=sku)
        stock = get_object_or_404(Stock,product_detail=product_detail)
        quantity = stock.quantity

        template = 'store/barcode.html'
        context = {'product_detail':product_detail,'range':range(quantity),'quantity':quantity}

        context = {
            **context,
            **admin.site.each_context(request),

        }
        return render(request, template, context)




class ProductListView(LoginRequiredMixin, View):

    def get(self,request):
        product_list = Product.objects.all()
        product_form = ProductForm()

        DetailFormSet = inlineformset_factory(Product, ProductDetail,  fields='__all__' , can_delete_extra=True , extra=6)
        formset = DetailFormSet()
        context = {'product_list':product_list,
                   'product_form':product_form,
                   'formset':formset ,
                   }

        return render(request, 'store/product_list.html', context=context)

def addProduct(request):

        product_form = ProductForm()
        category_form = CategoryForm()


        context = {
                   'product_form':product_form,
                   'category_form':category_form,

                   }

        return render(request, 'store/add_product.html', context=context)

