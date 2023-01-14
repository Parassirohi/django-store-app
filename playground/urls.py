from django.urls import path
from . import views,views1,views2

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    # path('collection/', views.list_collection),
    # path('product/', views.product_view),
    # path('order/', views.order_view),
    # path('orderitem/',views.order_item_view),
]
