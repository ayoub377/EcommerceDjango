from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.Order_create, name='Order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.render_pdf, name='render_pdf')
]
