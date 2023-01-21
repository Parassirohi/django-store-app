from django.urls import path
from django.urls.conf import include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views
# URLConf
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-image')
# we overriden the get queryset method here we have to set the base name

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls








# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view()),


    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_detail),
    # path('collections/', views.collection_list),
    # path('collections/<int:pk>/', views.collection_detail)

    # path('collection/', views.list_collection),
    # path('product/', views.product_view),
    # path('order/', views.order_view),
    # path('orderitem/',views.order_item_view),
# ]
