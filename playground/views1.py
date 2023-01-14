from django.shortcuts import render
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F
from django.contrib.contenttypes.models import ContentType
from store.models import Product,OrderItem,Order, Customer,Collection

# def say_hello(request):
#     queryset = Product.objects.filter(
#         id__in=OrderItem.objects.values("product__id").distinct()).order_by('title')# to get rid of duplicate we used distinct())
#
#     context = {
#         'name':'Paras',
#         'products': list(queryset)
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Order.objects.select_related(
#         'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
#     # orderitem_set is way to reverse order inbuilt in python
#     # we use select_related() method only selected those related field which are mentioned
#     #  when other end of the relationship has one instance select_related(1)
#     # But we use prefetch_related(n) when one end of the relationship has many object
#     context = {
#         'name':'Paras',
#         'orders':list(queryset)
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     result = Order.objects.aggregate(count = Count('id'))
#     # aggregate() use to summary the product
#     context = {
#         'name' : 'Paras',
#         'result': result
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     result = OrderItem.objects.filter(product__id=1).aggregate(unit_sold=Sum('quantity'))
#     context = {
#         'name' : 'Paras',
#         'result': result
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     result = Order.objects.filter(customer__id=1).aggregate(count= Count('id'))
#     context = {
#         'name' : 'Paras',
#         'result': result
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     result = Product.objects.filter(collection__id=3).aggregate\
#         (min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))
#     context = {
#         'name' : 'Paras',
#         'result': result
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Customer.objects.annotate(last_order_id=Max('order__id'))
#     # we use annotation() whenever we want to add a new field to a class
#     context = {
#         'name' : 'Paras',
#         'result': queryset
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Collection.objects.annotate(product_count=Count('product'))
#     context = {
#         'name' : 'Paras',
#         'result': queryset
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Customer.objects.annotate(order_count=Count('order')).filter(order_count__gt=5)
#     context = {
#         'name' : 'Paras',
#         'result': queryset
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Customer.objects.annotate\
#         (total_spend=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')))
#     context = {
#         'name' : 'Paras',
#         'result': queryset
#     }
#     return render(request, 'hello.html', context)

# def say_hello(request):
#     queryset = Product.objects.annotate(
#         total_sales=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))).order_by('-total_sales')[:5]
#     context = {
#         'name' : 'Paras',
#         'result': queryset
#     }
#     return render(request, 'hello.html', context)

