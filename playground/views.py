from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from django.db import transaction
from store.models import Order,OrderItem,Product,Customer,Collection, Cart, CartItem


# Badheadererror protect us from attackers
# def say_hello(request):
#     try:
#         # send_mail('subject', 'message', 'info@parasbuy.com', ['bob@parasbuy.com']) # send email to anyone
#         # mail_admins('subject', 'message', html_message='message', )
#         # for this to work we need to configure our site admin, got to setting module here we define our site admin
#         # message = EmailMessage('subject', 'message', 'info@parasbuy.com', ['bob@parasbuy.com'])
#         # message.attach_file('playground/static/images/temple.jpeg')
#         # message.send()
#
#         # after storing message in templates do this below
#         message = BaseEmailMessage(
#             template_name='emails/hello.html',
#             context={'name': 'Paras'},
#
#         )
#         message.send(['john@parasbuy.com'])
#     except BadHeaderError:
#         pass
#
#     return render(request, 'hello.html', {'name': 'Paras'})


#  sending emails with celery
def say_hello(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Paras'})







# def say_hello(request):
#     # For creating new object in database
#     collection = Collection()
#     collection.title = 'Video Game'
#     collection.featured_product = Product(pk=1)
#     collection.save()
#
#     return render(request, 'hello.html', {'name':'Paras'})

# def say_hello(request):
    # For updating in database
    # collection = Collection.objects.get(pk=11)
    # # First we are reading this object before updating.
    # collection.featured_product = None
    # collection.save()

    # One another way to update without reading object first
    # Collection.objects.filter(pk=1).update(featured_product=None)
    # return render(request, 'hello.html', {'name':'Paras'})

# def say_hello(request):
#     collection = Collection(pk=1)
#     # For deleting a single object
#     collection.delete()
#     # For deleting multiple object
#     Collection.object.filter(id__gt=5).delete()
#     return render(request, 'hello.html', {'name': 'Paras'})

# def say_hello(request):
#     # Creating a shopping cart with item
#     cart = Cart()
#     cart.save()
#
#     item1 = CartItem()
#     item1.cart = cart
#     item1.product_id = 1
#     item1.quantity = 1
#     item1.save()
#     return render(request, 'hello.html', {'name': 'Paras'})

# def say_hello(request):
#     # Update the quantity of an item
#     cartitem_quantity = CartItem.objects.get(pk=1)
#     cartitem_quantity.quantity = 2
#     cartitem_quantity.save()
#     return render(request, 'hello.html', {'name': 'Paras'})
#
# def say_hello(request):
#     # Removing a cart
#     cart = Cart(pk=1)
#     cart.delete()
#     # because we have enabled CASCADE in the relationship between cart and it's items,
#     # deleting a cart automatically causes deletion of it's items.
#     # So we don't need to delete each item individually
#     return render(request, 'hello.html', {'name': 'Paras'})


# Transcations:- sometimes we want multiple changes to our database , all changes should change together
# Or if one changes fails, then all changes should be rolled back.

# @transaction.atomic() # we can use as a decorator or a context manager, so we can apply this decorator
# to this view function and this wrap this entire function inside a transaction
# def say_hello(request):
#
#     # we can use this as a context manager if we want only some code inside a transaction
#     with transaction.atomic(): # as a context manager
#         order = Order()
#         order.customer_id = 1
#         # We always create parent record first before we can create child record
#         order.save()
#
#         item= OrderItem()
#         item.order = order
#         item.product_id = 1
#         item.quantity = 1
#         item.unit_price = 10
#         item.save()
#     return render(request, 'hello.html', {'name': 'Paras'})
#


