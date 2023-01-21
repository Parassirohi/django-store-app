from abc import ABC

from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage
from .signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField()


class ProductImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # we don't return product_id here because it's already in url -product/1/image/1

# we don't need to include product_id in our form coz we already have in our url,
# so when created product image object we should extract product id from url and use it to save product image


class ProductSerializer(serializers.ModelSerializer):
    # WE use model-serializer instead of serializer relationship.

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection', 'images']
        # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # class ProductSerializer(serializers.Serializer):
    #     id = serializers.IntegerField()
    #     title = serializers.CharField(max_length=255)
    #     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # we also  rename of any field by adding source in argument
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # We can also show extra field on our server without adding it to data.models like we do here(price_with_tax)
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # collection = serializers.StringRelatedField()
    # another way is to return a collections a string

    # collection = CollectionSerializer() # this is nested way to relate object
    # When returning a product we can also include related object like a collection

    def calculate_tax(self, product):  # we can also use product:Product if dont get intellisense like
        # here we add unit_price for that we use type annotation. __|
        return product.unit_price * Decimal(1.1)

    # def validators(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password does not match')
    #     return data
    # we use this field when password doesn't match now in this product we don't need that


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

        # we gonna override create method to creating a review

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    # we can reuse this in other situations where we want to return basic information
    # about a product like id,title nothing more. we created this if we want to add a single or multiple
    # products object not all, to other serialize  we just call this
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # even though our cart item model has product_id attributes this attributes generated
    # dynamically at runtime. it's not a field we reference here, so we have to
    # explicitly define this field

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with this given the given ID was found.")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        # If we want to add the same product to the same cart multiple times,
        # we don't want to create multiple cart item records. we want to update the quantity of an existing item

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item  # self.instance is a method of save
            # update an existing item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,
                                                    **self.validated_data)  # to unpack product_id and quantity
            # Create new item
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() # With this serializer we only serialize the critical information about the
    # product

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'payment_status'
        ]


class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic(): # we use transaction if our database goes offline in between creating database,
        # then we stuck for avoiding that we use transaction
        cart_id = serializers.UUIDField()
        # we don't use ModelSerializer,
        # coz we don't have order_id field in order class and to create an order we need order_id.

        def validate_cart_id(self, cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError('No cart with this cart id was found.')
            if CartItem.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('The cart is empty.')
            return cart_id

        def save(self, **kwargs): # we need override the save method because this logic for saving an order is very
            # specific. It's not something we want django to generate for us.
            # we need to go shopping cart table. we have to grab all cart items,
            # move them to order id table and then delete the shopping cart
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_item = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_item)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order) # this object have couples of method for sending
            # a signal,
            # send and send_robust, the difference is that if one of the receiver fails and throw an exception
            # the other receiver are not notified.
            # here we have an argument called sender this is a class that is sending the signal,
            # we use (self.__class__) this is magic attributes that returns class of current instance

            return order


