from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('add1/<int:product_id>/', views.cart_Add_list, name='cart_add list'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/', views.cart_update, name='cart_update'),
    path('update-shipping-cost/', views.cart_update_shipping_cost, name='cart_update_shipping_cost')
]
