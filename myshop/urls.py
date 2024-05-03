from django.urls import path

from .views import (
    HomeView,
    ProductDetailView, product_search_view,
    ProductListView

)

app_name = 'myshop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:id>/<slug:categor_slug>/', ProductListView.as_view(),
         name='product_list_by_category'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='details_product'),
    path('search/', product_search_view, name='product_search'),
]
