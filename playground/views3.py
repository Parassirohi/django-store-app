# from django.core import serializers
# from django.shortcuts import render
# from django.db.models import Q
# # from django.http import HttpResponse
# # from django.core.exceptions import ObjectDoesNotExist
# from store.models import Product,Customer,Collection,Order,OrderItem
# from json import dumps
#
#
#
# def say_hello(request):
#     # product: for inventory <10 and price < 20 we do
#     # Product.object.filter(inventory__lt=20).filter(unit_price__lt=20)
#
#     # product: inventory  <10 or price <20 (we import Q form django.db.models and use it we see below)
#     # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
#
#     # if we need product: inventory = unit_price
#     # from django.db.models import F
#     # Product.object.filter(inventory = F('unit_price')
#
#     # for sorting we use order_by() method we get queryset object, and we sort in ASC order, if we are accessing
#     # an individual object we don't get queryset
#     # product = Product.objects.order_by('title')[0] # we don't need list if we are accessing single object
#     # if we use .earliest instead of order_by we get the first element
#     # and by using .latest we sort in DEC order and get last object
#
#     queryset = Product.objects.values_list('id', 'title', 'collection__title')#by using values() method we can specific the field we wanna query
#     # if we use values_list() we got tuple instead of dictionary
#     context = {
#         'name': "Paras",
#         'products': list(queryset)
#     }
#     return render(request, 'hello.html', context)
#
# # def list_collection(request):
# #     queryset = Collection.objects.filter(featured_product_id__isnull=True)
# #     context = {
# #         'name': 'Paras',
# #         'collections': queryset,
# #     }
# #     return render(request, "collection.html", context)
# #
# # def product_view(request):
# #     queryset = Product.objects.filter(inventory__lt=10)
# #     context = {
# #         'name':'Paras',
# #         'products': queryset,
# #     }
# #     return render(request, "product.html", context)
# #
# # def order_view(request):
# #     queryset = Order.objects.filter(customer__id=1)
# #     context = {
# #         "name":"Paras",
# #         "orders":queryset
# #     }
# #     return render(request,"order.html", context)
# #
# # def order_item_view(request):
# #     queryset = OrderItem.objects.filter(product__collection__id=3)
# #     print(queryset)
# #     context = {
# #         'name':'Paras',
# #         'order_items':queryset
# #     }
# #
# #
# #     return render(request, 'order_item.html', context)