from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection, OrderItem, Review
from .serializer import CollectionSerializer, ProductSerializer, ReviewSerializer

# Create your views here.

# Combined logics for multiple related views inside a single class that's why it called view sets.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id'] # generic filtering

    # def get_queryset(self): # filtering a specific field
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request':self.request}

# we use destroy method instead of delete in ModelViewSet,
    def destroy(self, request, *args, **kwargs):
            # product is already retrieve we don't want to retrieve it twice,
            # so we change our validation logic and rewrite it like this
        if OrderItem.objects.filter(product_id=['pk']).count() > 0:
            return Response({'error':'Product cannot be deleted because it is associated with an order item'}
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
    serializer_class = CollectionSerializer(read_only=True)

    def delete(self,request,pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product.count() > 0 :
            return Response({'error':'Collection cannot be deleted because it include one or more product'}
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
