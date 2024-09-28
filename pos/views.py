import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError, transaction
import datetime

from django.shortcuts import render

from .models import Order

# Create your views here.


from django.views.generic import View
from django.http import JsonResponse
from store.models import Product, ProductDetail, Stock
from .models import *
from django.contrib import admin
from django.db.models import Sum, F
from django.contrib import admin


@transaction.atomic
def CreateOrderView( request):
        try:
            response_json = request.POST.dict()
            response_json = json.dumps(response_json)
            data = json.loads(response_json)


            order_items = json.loads(data['order_items'])


            # Verify that that quantities are available in stock
            instock = True
            for o_item in order_items:
                product_detail = ProductDetail.objects.get(id=o_item['product_id'])
                if(Stock.objects.filter(product_detail=product_detail).exists()==False):
                    instock = False
                    return JsonResponse({"error": "Stock Error: Product:- "+str(product_detail.product.name)+" with Size:- "+str(product_detail.size)+" is not registered in stock"}, status=404)

                stock = Stock.objects.get(product_detail=product_detail)

                if (stock.quantity < int(o_item['quantity']) ):
                    instock = False

            if (instock==False):
                return JsonResponse({"error": "Quantity Error: trying to sale products out of stock"}, status=404)

            with transaction.atomic():

                # Create the order
                order = Order.objects.create(user=request.user)
                sum = 0

                for o_item in order_items:
                    product_detail = ProductDetail.objects.get(id=o_item['product_id'])
                    stock = Stock.objects.get(product_detail=product_detail)

                    # Create order items
                    sub_total = int( o_item['quantity'] ) * float(o_item['product_price'])
                    sum = sum + sub_total
                    print(o_item['quantity'])
                    order_item = OrderItem.objects.create(order=order, stock=stock, quantity=o_item['quantity'],
                                                      unit_price=float(o_item['product_price']),
                                                      cost_price=product_detail.cost_price,
                                                      total_amount=sub_total)


                    # decreament from stock
                    stock.quantity = stock.quantity - int(o_item['quantity'])

                    # save changes
                    stock.save()
                    order.total_amount = sum
                    order.save()

            # Return a JSON response with the order details
            return JsonResponse({
                'id': order.id,
                'total_amount': order.total_amount,
                'created_at': order.created_at.isoformat()
            })
        except (IntegrityError):
            # Handle the case where the product or stock information is not found
            return JsonResponse({"error": "Quantity Error: trying to sale products out of stock"}, status=404)
        except MultipleObjectsReturned:

            return JsonResponse({"error": "Multiple stock record with on detail . Please fix!"}, status=404)
        except Exception:
            return JsonResponse({"error": "Internal Error . Please Report!"}, status=500)


class VoidOrderItemsView(View):

    def get(self, request):
        try:
            order_data = request.GET.dict()
            print(order_data)
            counter = 1
            order_items = []
            temp = {}
            for k, v in order_data.items():
                if 'product_id' in k:
                    temp['product_id'] = int(v)
                elif 'quantity' in k:
                    temp['quantity'] = int(v)
                    order_items.append(temp)
                    temp = {}

            print(order_items)

            # no need to Verify that that quantities are available in stock
            # Create the order
            order = Order.objects.create(user=request.user,isvoid=True)

            sum = 0

            for o_item in order_items:
                product_detail = ProductDetail.objects.get(id=o_item['product_id'])
                stock = Stock.objects.get(product_detail=product_detail)

                # Create order items
                sub_total = o_item['quantity'] * product_detail.unit_price
                sum = sum + sub_total

                order_item = OrderItem.objects.create(order=order, stock=stock, quantity=o_item['quantity'],
                                                      unit_price=product_detail.unit_price,
                                                      cost_price=product_detail.cost_price,
                                                      total_amount=sub_total, isvoid=True)

                print(23232)
                # decreament from stock
                stock.quantity = stock.quantity + o_item['quantity']

                # save changes
                stock.save()
            order.total_amount = sum
            order.save()

            # Return a JSON response with the order details
            return JsonResponse({
                'id': order.id,
                'total_amount': order.total_amount,
                'created_at': order.created_at.isoformat()
            })
        except (IntegrityError):
            # Handle the case where the product or stock information is not found
            return JsonResponse({"error": "Quantity Error: trying to sale products out of stock"}, status=404)
        except MultipleObjectsReturned:

            return JsonResponse({"error": "Multiple stock record with on detail . Please fix!"}, status=404)





def sales(request, *args, **kwargs):

    start_date = request.GET.get('start_date', default=datetime.date.today())
    end_date = request.GET.get('end_date', default=datetime.date.today())
    if (start_date == "" or end_date == ""):
        start_date = datetime.date.today()
        end_date = datetime.date.today()
    # Build the queryset with filters
    queryset = Order.objects.prefetch_related('orderitem_set')
    queryset_all = queryset.filter(created_at__gte=start_date,created_at__lte=end_date)
    print(2,start_date, end_date)
    if start_date:
        queryset1 = queryset.filter(created_at__gte=start_date, isvoid=True)
    if end_date:
        queryset1 = queryset1.filter(created_at__lte=end_date, isvoid=True)
    print(queryset1)

    if start_date:
        queryset = queryset.filter(created_at__gte=start_date, isvoid=False)
    if end_date:
        queryset = queryset.filter(created_at__lte=end_date,  isvoid=False)



    total_amount = queryset.aggregate(Sum('orderitem__total_amount'))['orderitem__total_amount__sum'] or 0

    # Calculate the cost of items, selling price, and profit or loss

    queryset = queryset.annotate(
        cost_price=Sum(F('orderitem__cost_price') * F('orderitem__quantity')),
        selling_price=Sum(F('orderitem__unit_price') * F('orderitem__quantity')),
    )
    queryset_all = queryset_all.annotate(
        cost_price=Sum(F('orderitem__cost_price') * F('orderitem__quantity')),
        selling_price=Sum(F('orderitem__unit_price') * F('orderitem__quantity')),
    )

    # Calculate total profit/loss

    total_cost = queryset.aggregate(Sum('cost_price'))['cost_price__sum'] or 0
    total_price = queryset.aggregate(Sum('selling_price'))['selling_price__sum'] or 0


    # for void
    total_amount1 = queryset1.aggregate(Sum('orderitem__total_amount'))['orderitem__total_amount__sum'] or 0

    # Calculate the cost of items, selling price, and profit or loss

    queryset1 = queryset1.annotate(
        cost_price=Sum(F('orderitem__cost_price') * F('orderitem__quantity')),
        selling_price=Sum(F('orderitem__unit_price') * F('orderitem__quantity')),
    )

    # Calculate total profit/loss
    total_cost1 = queryset1.aggregate(Sum('cost_price'))['cost_price__sum'] or 0
    total_price1 = queryset1.aggregate(Sum('selling_price'))['selling_price__sum'] or 0

    total_profit_loss = total_price - total_cost
    total_profit_loss1 = total_price1 - total_cost1
    context = {
        'orders': queryset_all,
        'total_amount': total_amount - total_amount1,
        'total_profit_loss': total_profit_loss - total_profit_loss1,
        'total_cost': total_cost ,
        'total_price': total_price ,
        'start_date': start_date,
        'end_date': end_date,

        'orders1': queryset1,
        'total_amount1': total_amount1,
        'total_cost1': total_cost1,
        'total_price1': total_price1,
    }

    # Add additional context data
    context = {
        **context,
        **admin.site.each_context(request),
        "opts": Order._meta,
    }

    return render(request, 'pos/pos_sales.html', context)

@login_required(login_url='login')
def help(request):
    context = {

        **admin.site.each_context(request),


    }
    products  = Product.objects.all()

    for p in products:

        filtered_p = Product.objects.filter(name = p.name)
        #print("prduct more than one", p.id, p.name, counts)
        if (len(filtered_p) >1):
            for f_p in filtered_p:
                product_detail = ProductDetail.objects.filter(product=p).count()
                print("prduct more than one", f_p.id, f_p.name, product_detail)



    return render(request, 'help/help.html',context)
