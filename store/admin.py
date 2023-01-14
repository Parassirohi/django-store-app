from tags.models import TaggedItem
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from tags.models import TaggedItem
from . import models
# Register your models here.
@admin.register(models.Collection)
@admin.display(ordering='product_count')
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'product_count']

    def product_count(self, collection):
        # return collection.product_count # we don't have field with this name in collection
    # for that we need to override queryset on this page and annotate product_count

        url = (reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                    'collection__id': str(collection.id)
                })) # this is where we need to generate the query string parameters to apply filter,
        # for that we import
        #another utility function urlencode
        return format_html('<a href="{}"> {} </a>', url, collection.product_count) # to provide
        # link to product we use format_html


    # there is no filter on product list to apply a filter we need to add (?collection__id=1) into url

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('products')
        )



class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

#customisation the list
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title'] # we are passing a list, so we can add multiple fields
    }

    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status','collection_title'] # used to display given object, we can
    # also add related object to our display, like we add collection and if we want to show special field
    # for that we need to define method by that name
    list_editable = ['unit_price']# used to edit given list object
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    # add new field to product display using computed column
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description= 'Clear inventory')
    def clear_inventory(self, request, queryset):  # we are defining this function to add
                                                    # more option in admin's action
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product were successfully updated.',
            messages.ERROR
        )



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_field = ['first_name__istartswith']
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] # i for instances



class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    max_num = 10
    autocomplete_fields = ['product']
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']


# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin) # we can one way and second way on above

