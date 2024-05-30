from django.urls import path

from account.views import edit_review
from .views import (
    HomeView,
    ProductDetailView, product_search_view,
    ProductListView,
    contact, politique, quick_view, subscribe

)

app_name = 'myshop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:id>/<slug:categor_slug>/', ProductListView.as_view(),
         name='product_list_by_category'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='details_product'),
    path('search/', product_search_view, name='product_search'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('contact/', contact, name='contact_us'),
    path('politique/', politique, name='politique'),
    path('quick-view/<int:product_id>', quick_view, name='quick-view'),
    path('subscribe/', subscribe, name='newsletter-subscribe'),
]
