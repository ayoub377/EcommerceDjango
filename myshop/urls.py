from django.urls import path

from . import views

app_name = 'myshop'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id><slug:categor_slug>/', views.list_prods_categories,
         name='product_list_by_category'),
    path('<int:id><slug:categor_slug>', views.range_filter,
         name='range_filter'),
    path('details/<int:pk>/', views.details, name='details_product'),
    path('search/', views.product_search, name='product_search'),
    path('search_auto/', views.search_auto, name='search_auto')
]
