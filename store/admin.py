# from django.contrib.contenttypes.admin import GenericTabularInline
# from tags.models import TaggedItem
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


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
                }))  # this is where we need to generate the query string parameters to apply filter,
        # for that we import
        # another utility function urlencode
        return format_html('<a href="{}"> {} </a>', url, collection.product_count)  # to provide
        # link to product we use format_html

    # there is no filter on product list to apply a filter we need to add (?collection__id=1) into url

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('products')
        )


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage  # register this with admin class
    readonly_fields = ['thumbnail']

    # thumbnail is not one of the fields of the product image claSS, so we need to define method

    def thumbnail(self, instance):  # now we take that product image and convert it to an HTML page
        if instance.image.name != '':  # we use condition to check whether we have image or not
            return format_html(f'<img src="{instance.image.url}" class="custom-thumbnail" />')
        # we use format_html here coz we only get url not an image in our admin thumbnail,
        # now this image is way too big this is where we use css, this is a css class that we define in static folder
        return ''


# customisation the list
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [TagInline]
    inlines = [ProductImageInline]

    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']  # we are passing a list, so we can add multiple fields
    }

    actions = ['clear_inventory']
    list_filter = ['collection', 'last_update', InventoryFilter]

    list_display = ['title', 'unit_price', 'inventory_status',
                    'collection_title']  # used to display given object, we can
    # also add related object to our display, like we add collection and if we want to show special field
    # for that we need to define method by that name
    list_editable = ['unit_price']  # used to edit given list object
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

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):  # we are defining this function to add
        # more option in admin's action
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product were successfully updated.',
            messages.ERROR
        )

    class Media:  # with this class we can specify the static assets that should be loaded on the product admin page
        # , we can load css or jawa script file. this class just like Meta class.
        css = {
            'all': ['store/styles.css']
        } # this is how we can load our style sheet or our css file on the product admin page


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
            'customer__id': str(customer.id)
        }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


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
