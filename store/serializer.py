from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    # WE use model-serializer instead of serializer relationship.
    class Meta:
        model = Product
        fields = ['id', 'title','description','slug', 'inventory', 'unit_price','price_with_tax', 'collection']
        # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # we also  rename of any field by adding source in argument
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#We can also show extra field on our server without adding it to data.models like we do here(price_with_tax)
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # collection = serializers.StringRelatedField()
    # another way is to return a collections a string

    # collection = CollectionSerializer() # this is nested way to relate object
    # When returning a product we can also include related object like a collection

    def calculate_tax(self, product): # we can also use product:Product if dont get intellisense like
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