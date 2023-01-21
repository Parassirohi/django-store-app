from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count

from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAdminUser
from rest_framework.views import APIView

from store.pagination import DefaultPagination
from .models import Product, Collection, OrderItem, Review, CartItem, Cart, Customer, Order, ProductImage
from .serializer import CollectionSerializer, ProductSerializer, ReviewSerializer, \
    CartSerializer, CartItemSerializer, AddCartItemSerializer, \
    UpdateCartItemSerializer, CustomerSerializer, OrderSerializer,\
    CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermissions


# Create your views here.

# Combined logics for multiple related views inside a single class that's why it called view sets.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter  # generic filtering
    # filterset_fields = ['collection_id'] # we can also add more fields in this
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self): # filtering a specific field
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    # we use destroy method instead of delete in ModelViewSet,
    def destroy(self, request, *args, **kwargs):
        # product is already retrieve we don't want to retrieve it twice,
        # so we change our validation logic and rewrite it like this
        if OrderItem.objects.filter(product_id=['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}
                            , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error':'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


#  CLASS BASED VIEWS
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
#     # if we have some logic for creating a queryset or serializer we use function to implement those logics,
#     # but if we don't have any specific logic we simply wanna return an expression
#     # we can use these attributes (as shown above)
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
#     #
#     # def get_serializer(self, *args, **kwargs):
#     #     return ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request':self.request}


# It's is a generic views
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # def get(self, request, id):# class based views
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # def put(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error':'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#  View Set

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more product'}
                            , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generic views
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('products')).all()
#     serializer_class = CollectionSerializer(read_only=True)
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('products'))
#     serializer_class = CollectionSerializer
#
#     def delete(self,request,pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.product.count() > 0 :
#             return Response({'error':'Collection cannot be deleted because it include one or more product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # THESE ARE FUNCTION BASED VIEWS
# @api_view(['GET', 'POST']) # for deserializer we use both post and get as an argument in decorator,
# # by default it takes GET method, but now we are passing POST, so we have to pass both
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related('collection').all() # we use select_related because
#     # we are using string related to convert each collection into a string serializer to load page fast
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data) # previously we pass queryset or product for serializer,
#         # to deserializer we have to set data=request.data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request,id):
#     product = get_object_or_404(Product,pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#     # we create serializer and give it this product object,
#         return Response(serializer.data)
#     # this serializer convert our product object to a dictionary,
#     # and we can get that dict. from serialize data.
#
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         if product.orderitems.count()>0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(product_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# #
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#         product_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error':'Collection cannot be deleted because it include one or more product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # if we use .all() we get the same review for all products instead using all we use .filter()

    # we want to read the product of a review from urls for that we create a context object
    # to pass it through a serializer
    # we create context to provide additional data to our serializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    # pass this dictionary to our serializer


# Cart
# we don't need list,update operation, so we are going to create a custom view set instead ModelViewSet
# through Mixin
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related(
        'items__product').all()  # we use prefetch method coz we have multiple items,
    # and for foreign keys where we have a single related object there we use select_related.
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    # we don't wanna hardcore cart item serializer. we want to dynamically return a serializer
    # class depending on request method, so we want to override, get serializer class.

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    # we can get cart_id from url, so

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']).select_related(
            'product')  # we use self.kwargs coz we need id from our url


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermissions])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'],
            permission_classes=[IsAuthenticated])  # if its false it means this action is available to ListView,
    # if it's true it means this
    # action gonna be available on the DetailView
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    # Getting or updating current user profile


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    # serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):  # context means = when you want to add extra data to the serializer in
    #     # addition to the object being serialized.
    #
    #     return {'user_id': self.request.user.id}
    # this method is only useful if we want to rely on create order mixin that we inherit in this class,
    # but now we have created our new create method from scratch.

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(
            # now we are using signals we don't need to worry about creating a customer by(get_or_create)
            user_id=self.request.user.id)  # here we get a complete customer object
        # but we need only customer id
        return Order.objects.filter(customer_id=customer_id)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])  # we get the product id from url
        # we don't return images or all product's images in a database,
        # we only ant to return the images for a particular product, so we gonna override get_queryset

